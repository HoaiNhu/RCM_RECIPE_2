# infrastructure/ml_models/trend_predictor.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import json
from pathlib import Path

class TrendPredictor:
    """
    Mô hình ML dự đoán xu hướng bánh ngọt dựa trên:
    - Dữ liệu lịch sử từ YouTube trends
    - Thông tin mùa vụ, sự kiện
    - Phân khúc khách hàng
    - Thời tiết, lễ hội
    """
    
    def __init__(self, model_path: Optional[Path] = None, auto_load: bool = True):
        self.model_path = model_path or Path("data/models")
        self.model_path.mkdir(exist_ok=True, parents=True)
        
        # Models cho từng task
        self.popularity_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.engagement_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.trend_classifier = RandomForestRegressor(n_estimators=50, random_state=42)
        
        # Preprocessors
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
        # Features được train
        self.feature_columns = []
        self.is_trained = False
        
        # Auto-load trained artifacts nếu có
        if auto_load:
            try:
                loaded = self.load_models()
                if loaded:
                    self.is_trained = True
            except Exception as e:
                print(f"⚠️ Auto-load models failed: {e}")
        
    def load_training_data(self, data_dir: Path) -> pd.DataFrame:
        """Load và merge tất cả dữ liệu training"""
        
        # Load main datasets
        trends_df = pd.read_csv(data_dir / "youtube_bakery_gaming_trends_cleaned.csv")
        consumer_df = pd.read_csv(data_dir / "consumer_groups_detailed_20250921_133329.csv") 
        seasonal_df = pd.read_csv(data_dir / "seasonal_trends_20250920_061904.csv")
        events_df = pd.read_csv(data_dir / "vietnam_seasonal_events_2025.csv")
        preferences_df = pd.read_csv(data_dir / "comprehensive_food_preferences_raw_20250920_074528.csv")
        
        print(f"Loaded datasets:")
        print(f"- YouTube trends: {len(trends_df)} records")
        print(f"- Consumer groups: {len(consumer_df)} records") 
        print(f"- Seasonal trends: {len(seasonal_df)} records")
        print(f"- Vietnam events: {len(events_df)} records")
        print(f"- Food preferences: {len(preferences_df)} records")
        
        # Bakery-only filter: giữ lại các bản ghi có liên quan food/bakery
        bakery_keywords = ['cake', 'bánh', 'dessert', 'bakery', 'chocolate', 'matcha', 'taro', 'mousse', 'cookie', 'macaron']
        def _is_bakery_row(row) -> bool:
            text = ' '.join([
                str(row.get('chu_de', '')),
                str(row.get('tu_khoa_tim_kiem', '')),
                str(row.get('tieu_de', '')),
                str(row.get('mo_ta', '')),
                str(row.get('tags', '')),
                str(row.get('banh_ngot_phat_hien', '')),
                str(row.get('banh_ngot_yeu_thich', ''))
            ]).lower()
            return any(kw in text for kw in bakery_keywords)

        try:
            before = len(trends_df)
            trends_df = trends_df[trends_df.apply(_is_bakery_row, axis=1)]
            print(f"Filtered YouTube trends to bakery-only: {before} -> {len(trends_df)}")
        except Exception as e:
            print(f"Warning: bakery filter failed: {e}")

        return self._merge_datasets(trends_df, consumer_df, seasonal_df, events_df, preferences_df)
    
    def _merge_datasets(self, trends_df, consumer_df, seasonal_df, events_df, preferences_df) -> pd.DataFrame:
        """Merge và prepare data cho training"""
        
        # Convert dates
        if 'ngay_dang' in trends_df.columns:
            trends_df['ngay_dang'] = pd.to_datetime(trends_df['ngay_dang'])
            trends_df['month'] = trends_df['ngay_dang'].dt.month
            trends_df['day_of_year'] = trends_df['ngay_dang'].dt.dayofyear
            trends_df['weekday'] = trends_df['ngay_dang'].dt.weekday
        
        if 'date' in events_df.columns:
            events_df['date'] = pd.to_datetime(events_df['date'])
            events_df['month'] = events_df['date'].dt.month
            events_df['day_of_year'] = events_df['date'].dt.dayofyear
        
        # Merge với seasonal data
        season_map = {
            1: 'Đông', 2: 'Đông', 3: 'Xuân', 4: 'Xuân', 5: 'Xuân',
            6: 'Hè', 7: 'Hè', 8: 'Hè', 9: 'Thu', 10: 'Thu', 11: 'Thu', 12: 'Đông'
        }
        
        # Prepare main training dataframe
        training_data = trends_df.copy()
        
        # Add seasonal features
        if 'month' in training_data.columns:
            training_data['season'] = training_data['month'].map(season_map)
        
        # Add event features (tính average cho mỗi tháng)
        if 'month' in training_data.columns and len(events_df) > 0:
            event_features = events_df.groupby('month').agg({
                'temperature_celsius': 'mean',
                'rainfall_probability': 'mean', 
                'vietnam_bakery_demand_factor': 'mean',
                'cold_drink_demand': 'mean',
                'hot_beverage_demand': 'mean',
                'ice_cream_cake_demand': 'mean',
                'domestic_tourism_factor': 'mean'
            }).reset_index()
            
            training_data = training_data.merge(event_features, on='month', how='left')
        
        # Add consumer insights (map với nhóm đối tượng)
        if 'nhom_doi_tuong' in training_data.columns:
            consumer_map = {}
            for _, row in consumer_df.iterrows():
                consumer_map[row['consumer_group']] = {
                    'market_potential_score': 1 if row['market_potential'] == 'Cao' else 0.5,
                    'competition_level_score': 1 if row['competition_level'] == 'Rất cao' else 0.5,
                    'growth_trend_score': 1 if 'Tăng' in str(row['growth_trend']) else 0,
                    'avg_engagement': row['avg_engagement_rate']
                }
            
            # Map consumer features
            training_data['market_potential_score'] = training_data['nhom_doi_tuong'].map(
                lambda x: consumer_map.get(x, {}).get('market_potential_score', 0.5)
            )
            training_data['competition_level_score'] = training_data['nhom_doi_tuong'].map(
                lambda x: consumer_map.get(x, {}).get('competition_level_score', 0.5)
            )
            training_data['growth_trend_score'] = training_data['nhom_doi_tuong'].map(
                lambda x: consumer_map.get(x, {}).get('growth_trend_score', 0)
            )
        
        # Clean missing values
        training_data = training_data.fillna(0)
        
        print(f"Final training data shape: {training_data.shape}")
        return training_data
    
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Chuẩn bị features cho training"""
        
        feature_df = df.copy()
        
        # Numerical features
        numerical_features = [
            'luot_xem', 'luot_thich', 'luot_binh_luan', 'engagement_rate_%',
            'so_ngay_tu_khi_dang', 'so_loai_thuc_pham', 'so_loai_banh_ngot',
            'diem_noi_tieng', 'month', 'day_of_year', 'weekday'
        ]
        
        # Add event features nếu có
        event_features = [
            'temperature_celsius', 'rainfall_probability', 'vietnam_bakery_demand_factor',
            'cold_drink_demand', 'hot_beverage_demand', 'ice_cream_cake_demand',
            'domestic_tourism_factor', 'market_potential_score', 'competition_level_score',
            'growth_trend_score'
        ]
        
        # Categorical features để encode
        categorical_features = ['chu_de', 'nhom_doi_tuong', 'muc_do_viral', 'season']
        
        # Select existing features only
        available_numerical = [f for f in numerical_features if f in feature_df.columns]
        available_event = [f for f in event_features if f in feature_df.columns]
        available_categorical = [f for f in categorical_features if f in feature_df.columns]
        
        # Create final feature set
        final_features = []
        
        # Add numerical features
        for feature in available_numerical:
            if feature_df[feature].dtype in ['int64', 'float64']:
                final_features.append(feature)
            else:
                # Convert to numeric nếu có thể
                feature_df[feature] = pd.to_numeric(feature_df[feature], errors='coerce')
                final_features.append(feature)
        
        # Add event features
        final_features.extend(available_event)
        
        # Encode categorical features
        for feature in available_categorical:
            if feature not in self.label_encoders:
                self.label_encoders[feature] = LabelEncoder()
                feature_df[f'{feature}_encoded'] = self.label_encoders[feature].fit_transform(
                    feature_df[feature].astype(str)
                )
            else:
                # Use fitted encoder
                feature_df[f'{feature}_encoded'] = self.label_encoders[feature].transform(
                    feature_df[feature].astype(str)
                )
            final_features.append(f'{feature}_encoded')
        
        # Create features for viral potential (special engineering)
        if 'luot_xem' in feature_df.columns and 'luot_thich' in feature_df.columns:
            feature_df['viral_potential'] = (
                feature_df['luot_thich'] / (feature_df['luot_xem'] + 1) * 100
            )
            final_features.append('viral_potential')
        
        if 'engagement_rate_%' in feature_df.columns:
            feature_df['engagement_category'] = pd.cut(
                feature_df['engagement_rate_%'], 
                bins=[-np.inf, 2, 4, 6, np.inf], 
                labels=[0, 1, 2, 3]
            ).astype(int)
            final_features.append('engagement_category')
        
        # Fill missing values
        feature_df[final_features] = feature_df[final_features].fillna(0)
        
        self.feature_columns = final_features
        print(f"Prepared {len(final_features)} features: {final_features}")
        
        return feature_df[final_features]
    
    def train(self, data_dir: Path):
        """Train models với time-based split và shifted targets để tránh leakage"""
        
        print("🚀 Bắt đầu training trend prediction models...")
        
        # Load data
        df = self.load_training_data(data_dir)

        # Time sort theo ngày đăng nếu có
        if 'ngay_dang' in df.columns:
            try:
                df = df.sort_values('ngay_dang')
            except Exception:
                pass

        # Shifted targets t+14 ngày (nếu có day_of_year)
        df_shift = df.copy()
        if 'day_of_year' in df_shift.columns:
            df_shift['day_of_year_shift'] = (df_shift['day_of_year'] + 14) % 366
        else:
            df_shift['day_of_year_shift'] = 0

        # Targets (không dùng các cột target thô như feature)
        targets = {}
        if 'luot_xem' in df_shift.columns:
            targets['popularity'] = np.log1p(df_shift['luot_xem'])
        if 'engagement_rate_%' in df_shift.columns:
            targets['engagement'] = df_shift['engagement_rate_%']
        if 'diem_noi_tieng' in df_shift.columns:
            targets['trend_score'] = df_shift['diem_noi_tieng']

        # Prepare features (drop direct target columns để giảm leakage)
        X = self.prepare_features(df_shift)
        for leak_col in ['luot_xem', 'diem_noi_tieng', 'engagement_rate_%']:
            if leak_col in self.feature_columns:
                self.feature_columns.remove(leak_col)
                X = X.drop(columns=[leak_col], errors='ignore')

        # Time-based split: 80% đầu làm train, 20% cuối làm test
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]

        # Fit scaler trên train
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Train và evaluate
        results = {}
        for target_name, y in targets.items():
            print(f"\n📊 Training {target_name} model (time-based split)...")
            y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

            if target_name == 'popularity':
                model = self.popularity_model
            elif target_name == 'engagement':
                model = self.engagement_model
            else:
                model = self.trend_classifier

            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            results[target_name] = {'mae': mae, 'r2': r2}
            print(f"✅ {target_name} - MAE: {mae:.4f}, R²: {r2:.4f}")

        self.is_trained = True
        self.save_models()
        return results
    
    def predict_trends(self, context: Dict) -> Dict:
        """Dự đoán xu hướng dựa trên context hiện tại"""
        
        if not self.is_trained:
            raise ValueError("Model chưa được train! Gọi train() trước.")
        
        # Tạo feature vector từ context (chuẩn theo feature_columns)
        feature_vector = self._context_to_features(context)

        # Biến thành DataFrame với tên cột đúng để tránh cảnh báo
        import pandas as pd
        feature_df = pd.DataFrame([feature_vector], columns=self.feature_columns)

        # Scale features
        feature_vector_scaled = self.scaler.transform(feature_df)
        
        # Predict
        predictions = {}
        predictions['popularity_score'] = float(self.popularity_model.predict(feature_vector_scaled)[0])
        predictions['engagement_score'] = float(self.engagement_model.predict(feature_vector_scaled)[0])
        predictions['trend_score'] = float(self.trend_classifier.predict(feature_vector_scaled)[0])
        
        # Calculate overall trend strength
        predictions['overall_trend_strength'] = (
            predictions['popularity_score'] * 0.4 +
            predictions['engagement_score'] * 0.3 +
            predictions['trend_score'] * 0.3
        )
        
        return predictions
    
    def _context_to_features(self, context: Dict) -> List[float]:
        """Convert context thành feature vector"""
        
        # Default feature vector
        features = [0.0] * len(self.feature_columns)
        
        # Map context to features
        feature_mapping = {
            'month': context.get('month', datetime.now().month),
            'day_of_year': context.get('day_of_year', datetime.now().timetuple().tm_yday),
            'weekday': context.get('weekday', datetime.now().weekday()),
            'temperature_celsius': context.get('temperature', 25.0),
            'rainfall_probability': context.get('rainfall_prob', 0.3),
            'vietnam_bakery_demand_factor': context.get('bakery_demand', 1.0),
            'cold_drink_demand': context.get('cold_drink_demand', 0.5),
            'hot_beverage_demand': context.get('hot_beverage_demand', 0.5),
            'ice_cream_cake_demand': context.get('ice_cream_demand', 0.5),
            'domestic_tourism_factor': context.get('tourism_factor', 1.0),
            'market_potential_score': context.get('market_potential', 0.7),
            'competition_level_score': context.get('competition_level', 0.6),
            'growth_trend_score': context.get('growth_trend', 1.0)
        }
        
        # Categorical mappings: encode an toàn nếu có label_encoders, tránh đưa chuỗi vào scaler
        if 'nhom_doi_tuong_encoded' in self.feature_columns:
            idx = self.feature_columns.index('nhom_doi_tuong_encoded')
            value = context.get('user_segment')
            try:
                encoder = self.label_encoders.get('nhom_doi_tuong')
                if encoder is not None and value is not None:
                    # Nếu giá trị chưa thấy trong encoder, dùng giá trị phổ biến 0
                    if value not in list(encoder.classes_):
                        features[idx] = 0
                    else:
                        features[idx] = float(encoder.transform([value])[0])
            except Exception:
                features[idx] = 0
        
        if 'season_encoded' in self.feature_columns:
            idx = self.feature_columns.index('season_encoded')
            value = context.get('season')
            try:
                encoder = self.label_encoders.get('season')
                if encoder is not None and value is not None:
                    if value not in list(encoder.classes_):
                        features[idx] = 0
                    else:
                        features[idx] = float(encoder.transform([value])[0])
            except Exception:
                features[idx] = 0
        
        # Fill in mapped features
        for feature_name, value in feature_mapping.items():
            if feature_name in self.feature_columns:
                idx = self.feature_columns.index(feature_name)
                features[idx] = float(value)
        
        return features
    
    def save_models(self):
        """Save trained models"""
        
        models_to_save = {
            'popularity_model': self.popularity_model,
            'engagement_model': self.engagement_model, 
            'trend_classifier': self.trend_classifier,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_columns': self.feature_columns
        }
        
        for name, model in models_to_save.items():
            joblib.dump(model, self.model_path / f"{name}.pkl")
        
        print(f"✅ Models saved to {self.model_path}")
    
    def load_models(self):
        """Load trained models"""
        
        try:
            self.popularity_model = joblib.load(self.model_path / "popularity_model.pkl")
            self.engagement_model = joblib.load(self.model_path / "engagement_model.pkl")
            self.trend_classifier = joblib.load(self.model_path / "trend_classifier.pkl")
            self.scaler = joblib.load(self.model_path / "scaler.pkl")
            self.label_encoders = joblib.load(self.model_path / "label_encoders.pkl")
            self.feature_columns = joblib.load(self.model_path / "feature_columns.pkl")
            
            self.is_trained = True
            print(f"✅ Models loaded from {self.model_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load models: {e}")
            return False

if __name__ == "__main__":
    # Test training
    data_dir = Path("data/raw")
    predictor = TrendPredictor()
    
    if data_dir.exists():
        results = predictor.train(data_dir)
        
        # Test prediction
        test_context = {
            'month': 10,  # October - Halloween season
            'temperature': 22.0,
            'user_segment': 'Gen Z',
            'season': 'Thu',
            'market_potential': 0.8
        }
        
        predictions = predictor.predict_trends(test_context)
        print(f"\n🔮 Predictions for October context: {predictions}")
    else:
        print("❌ Data directory không tồn tại!")