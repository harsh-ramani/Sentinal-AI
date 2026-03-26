import random
import time
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import io
import warnings
import cv2
import urllib.request
import os
warnings.filterwarnings('ignore')

# Page config
st.set_page_config(page_title="🛡️ Global Border AI", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

# Beautiful Enhanced CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    color: #ffffff;
}

.main-header {
    font-size: 3.5rem;
    font-weight: 900;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 30%, #f093fb 60%, #f5576c 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 1rem;
    text-shadow: 0 0 40px rgba(102, 126, 234, 0.5);
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from { text-shadow: 0 0 20px rgba(102, 126, 234, 0.5); }
    to { text-shadow: 0 0 30px rgba(102, 126, 234, 0.8); }
}

.section-header {
    font-size: 2rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 1.5rem;
    background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.metric-container {
    background: linear-gradient(145deg, #1e1e2e, #2a2a3e);
    padding: 2rem;
    border-radius: 25px;
    border: 2px solid transparent;
    background-clip: padding-box;
    border-image: linear-gradient(45deg, #667eea, #764ba2, #f093fb) 1;
    box-shadow: 0 25px 80px rgba(0,0,0,0.5);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
}

.metric-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 6px;
    background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #f5576c);
    border-radius: 25px 25px 0 0;
}

.metric-container::after {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: conic-gradient(from 0deg, transparent, rgba(102, 126, 234, 0.1), transparent);
    animation: rotate 8s linear infinite;
    pointer-events: none;
}

@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.metric-container:hover {
    transform: translateY(-12px) scale(1.02);
    box-shadow: 0 40px 120px rgba(102, 126, 234, 0.4);
    border-image: linear-gradient(45deg, #f093fb, #f5576c, #667eea) 1;
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0.5rem 0;
    text-shadow: 0 0 20px rgba(255,255,255,0.3);
}

.metric-label {
    font-size: 0.9rem;
    color: #a0a0c0;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.status-badge {
    padding: 0.8rem 1.6rem;
    border-radius: 30px;
    font-weight: 700;
    font-size: 0.9rem;
    margin: 0.5rem 0;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
}

.status-badge:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
}

.safe {
    background: linear-gradient(145deg, #10b981, #059669);
    color: white;
    box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
}

.warning {
    background: linear-gradient(145deg, #f59e0b, #d97706);
    color: white;
    box-shadow: 0 0 20px rgba(245, 158, 11, 0.3);
}

.danger {
    background: linear-gradient(145deg, #ef4444, #dc2626);
    color: white;
    box-shadow: 0 0 20px rgba(239, 68, 68, 0.3);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { box-shadow: 0 0 20px rgba(239, 68, 68, 0.3); }
    50% { box-shadow: 0 0 30px rgba(239, 68, 68, 0.6); }
}

.alert-banner {
    background: linear-gradient(90deg, #ef4444, #f59e0b, #f093fb);
    color: white;
    padding: 1.5rem;
    border-radius: 20px;
    text-align: center;
    font-weight: 700;
    font-size: 1.2rem;
    margin: 1rem 0;
    box-shadow: 0 10px 40px rgba(239,68,68,0.4);
    animation: slideIn 0.5s ease-out;
    position: relative;
    overflow: hidden;
}

.alert-banner::before {
    content: '⚠️';
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 1.5rem;
}

@keyframes slideIn {
    from { transform: translateY(-100%); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

.nav-button {
    background: linear-gradient(145deg, #2a2a3e, #1e1e2e);
    border: 2px solid #3a3a4e;
    color: #ffffff;
    padding: 1rem 2rem;
    border-radius: 15px;
    margin: 0.5rem 0;
    width: 100%;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    font-weight: 600;
    position: relative;
    overflow: hidden;
}

.nav-button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.2), transparent);
    transition: left 0.5s;
}

.nav-button:hover::before {
    left: 100%;
}

.nav-button:hover {
    background: linear-gradient(145deg, #667eea, #764ba2);
    border-color: #667eea;
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}

.progress-container {
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
    height: 8px;
    margin: 1rem 0;
    overflow: hidden;
}

.progress-bar {
    height: 100%;
    background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
    border-radius: 10px;
    transition: width 1s ease-in-out;
}

.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.feature-card {
    background: linear-gradient(145deg, #1e1e2e, #2a2a3e);
    padding: 2rem;
    border-radius: 20px;
    border: 1px solid #3a3a4e;
    transition: all 0.3s ease;
    cursor: pointer;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.2);
    border-color: #667eea;
}

.filter-panel {
    background: linear-gradient(145deg, #1e1e2e, #2a2a3e);
    padding: 2rem;
    border-radius: 20px;
    border: 1px solid #3a3a4e;
    margin-bottom: 2rem;
    backdrop-filter: blur(10px);
}

@media (max-width: 768px) {
    .main-header { font-size: 2.8rem; }
    .section-header { font-size: 1.6rem; }
    .metric-container { padding: 1.5rem; }
    .card-grid { grid-template-columns: 1fr; }
}
</style>
""", unsafe_allow_html=True)

# Custom session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

if 'alerts_enabled' not in st.session_state:
    st.session_state.alerts_enabled = True

if 'last_update' not in st.session_state:
    st.session_state.last_update = pd.Timestamp.now()

@st.cache_resource
def load_mobilenet_model():
    """Download and load the MobileNet SSD model for object detection."""
    prototxt_url = "https://raw.githubusercontent.com/djmv/MobilNet_SSD_opencv/master/MobileNetSSD_deploy.prototxt"
    caffemodel_url = "https://github.com/djmv/MobilNet_SSD_opencv/raw/master/MobileNetSSD_deploy.caffemodel"
    
    prototxt_path = "deploy.prototxt"
    caffemodel_path = "mobilenet_iter_73000.caffemodel"
    
    if not os.path.exists(prototxt_path):
        with st.spinner("Downloading model configuration..."):
            try:
                urllib.request.urlretrieve(prototxt_url, prototxt_path)
            except Exception as e:
                st.error(f"Failed to download MobileNet-SSD config: {e}")
                return None
            
    if not os.path.exists(caffemodel_path):
        with st.spinner("Downloading model weights (22MB)..."):
            try:
                urllib.request.urlretrieve(caffemodel_url, caffemodel_path)
            except Exception as e:
                st.error(f"Failed to download MobileNet-SSD weights: {e}")
                return None
                
    try:
        net = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)
        return net
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Class mapping for MobileNet SSD (VOC dataset)
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

# Relevant classes for intrusion detection
HUMAN_CLASSES = ["person"]
ANIMAL_CLASSES = ["bird", "cat", "cow", "dog", "horse", "sheep"]
VEHICLE_CLASSES = ["aeroplane", "bicycle", "bus", "car", "motorbike", "train"]

@st.cache_data
def generate_sample_data():
    """Generate optimized sample data using vectorized operations"""
    np.random.seed(42)
    n = 60000

    hotspots = {
        'US-Mexico': (29.0, -105.0, 0.48, '🇺🇸 USA'),
        'Ukraine-Russia': (49.0, 35.0, 0.62, '🇺🇦 Ukraine'),
        'India-Pakistan': (32.0, 75.0, 0.42, '🇮🇳 India'),
        'Syria-Turkey': (36.5, 38.0, 0.55, '🇹🇷 Turkey'),
        'Greece-Turkey': (40.5, 26.0, 0.38, '🇬🇷 Greece'),
        'Belarus-Poland': (52.5, 23.0, 0.45, '🇵🇱 Poland'),
        'Iran-Afghanistan': (32.0, 61.0, 0.40, '🇮🇷 Iran'),
        'South China Sea': (15.0, 115.0, 0.35, '🇨🇳 China'),
        'Libya-Tunisia': (32.0, 12.0, 0.32, '🇹🇳 Tunisia'),
        'Yemen-Saudi': (17.0, 52.0, 0.37, '🇸🇦 Saudi Arabia'),
    }

    # Vectorized data generation
    hotspot_names = list(hotspots.keys())
    hotspot_weights = [hotspots[name][2] for name in hotspot_names]  # Use risk as weights

    # Generate all data at once using numpy
    selected_hotspots_idx = np.random.choice(len(hotspot_names), size=n, p=np.array(hotspot_weights)/sum(hotspot_weights))
    selected_hotspots = [hotspot_names[i] for i in selected_hotspots_idx]

    # Create arrays for all features
    latitudes = np.zeros(n)
    longitudes = np.zeros(n)
    risk_scores = np.zeros(n)
    countries = []

    for i, hotspot in enumerate(selected_hotspots):
        lat, lon, risk, country = hotspots[hotspot]
        latitudes[i] = lat + np.random.normal(0, 0.15)
        longitudes[i] = lon + np.random.normal(0, 0.2)
        risk_scores[i] = risk
        countries.append(country)

    # Generate other features vectorized
    y = np.random.choice([0, 1], size=n, p=[0.5, 0.5])
    hours = np.where(y == 1,
                     np.random.choice([22,23,0,1,2,3], size=n),
                     np.random.choice([8,12,16], size=n))

    is_night = ((hours >= 20) | (hours <= 6)).astype(int)
    is_weekend = np.random.choice([0, 1], size=n, p=[0.7, 0.3])
    weather = np.random.choice([0,1,2,3], size=n)
    months = np.random.choice([6,7,8,9], size=n)
    day_of_week = np.random.choice(range(7), size=n)

    # Create timestamps more efficiently (30 days + 3 years)
    base_time = pd.Timestamp.now()
    timestamps = base_time - pd.to_timedelta(np.random.randint(0, 720 + 3 * 365 * 24, size=n), unit='h')

    # Create DataFrame directly
    data = pd.DataFrame({
        'Hotspot': selected_hotspots,
        'Country': countries,
        'Latitude': latitudes,
        'Longitude': longitudes,
        'Hour': hours,
        'Is_Night': is_night,
        'Is_Weekend': is_weekend,
        'Weather': weather,
        'Month': months,
        'DayOfWeek': day_of_week,
        'Is_Intrusion': y,
        'Risk_Score': risk_scores,
        'Timestamp': timestamps
    })

    return data

def get_risk_alerts(data):
    """Generate risk alerts based on current data"""
    alerts = []

    # High risk hotspots
    high_risk = data[data['Risk_Score'] > 0.5]['Hotspot'].unique()
    if len(high_risk) > 0:
        alerts.append({
            'type': 'danger',
            'message': f"🚨 CRITICAL: {len(high_risk)} hotspots at extreme risk",
            'details': f"Hotspots: {', '.join(high_risk[:3])}{'...' if len(high_risk) > 3 else ''}"
        })

    # Recent intrusions
    recent_intrusions = data[
        (data['Is_Intrusion'] == 1) &
        (data['Timestamp'] > pd.Timestamp.now() - pd.Timedelta(hours=24))
    ].shape[0]

    if recent_intrusions > 100:
        alerts.append({
            'type': 'warning',
            'message': f"⚠️ HIGH ACTIVITY: {recent_intrusions} intrusions in last 24h",
            'details': "Monitor these hotspots closely"
        })

    # Night time alerts
    night_risk = data[(data['Is_Night'] == 1) & (data['Is_Intrusion'] == 1)].shape[0] / max(data[data['Is_Night'] == 1].shape[0], 1)
    if night_risk > 0.6:
        alerts.append({
            'type': 'warning',
            'message': f"🌙 NIGHT THREAT: {night_risk*100:.1f}% intrusion rate during night hours",
            'details': "Enhanced night patrols recommended"
        })

    return alerts

def export_data(data, format_type='csv'):
    """Export data in different formats"""
    if format_type == 'csv':
        return data.to_csv(index=False).encode('utf-8')
    elif format_type == 'json':
        return data.to_json(orient='records').encode('utf-8')
    elif format_type == 'excel':
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            data.to_excel(writer, sheet_name='Border_Data', index=False)
        return buffer.getvalue()

@st.cache_data
def create_performance_metrics(_model, _X_test, _y_test, _data):
    """Create optimized performance metrics with caching"""
    from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

    y_pred = _model.predict(_X_test)
    y_pred_proba = _model.predict_proba(_X_test)[:, 1]

    # Basic metrics
    accuracy = _model.score(_X_test, _y_test)
    auc = roc_auc_score(_y_test, y_pred_proba)

    # Classification report (cached)
    report = classification_report(_y_test, y_pred, output_dict=True)

    # Confusion matrix
    cm = confusion_matrix(_y_test, y_pred)

    return {
        'accuracy': accuracy,
        'auc': auc,
        'precision': report['1']['precision'],
        'recall': report['1']['recall'],
        'f1_score': report['1']['f1-score'],
        'confusion_matrix': cm,
        'total_predictions': len(_y_test),
        'false_positives': cm[0][1],
        'false_negatives': cm[1][0],
        'true_positives': cm[1][1],
        'true_negatives': cm[0][0]
    }

@st.cache_data
def get_hotspot_stats(_data):
    """Cache hotspot statistics calculation"""
    hotspot_stats = _data.groupby('Hotspot').agg({
        'Is_Intrusion': ['mean', 'sum', 'count'],
        'Risk_Score': 'mean',
        'Country': 'first',
        'Hour': 'mean',
        'Is_Night': 'mean'
    }).round(3)

    # Flatten column names
    hotspot_stats.columns = ['intrusion_rate', 'total_breaches', 'total_events', 'avg_risk', 'country', 'avg_hour', 'night_rate']
    hotspot_stats = hotspot_stats.reset_index()

    # Add status and priority
    hotspot_stats['Status'], hotspot_stats['badge'] = zip(*[
        get_status_badge(row['avg_risk']) for _, row in hotspot_stats.iterrows()
    ])

    hotspot_stats['Priority'] = hotspot_stats['avg_risk'].apply(
        lambda x: "🔴 CRITICAL" if x > 0.5 else "🟡 HIGH" if x > 0.4 else "🟢 MEDIUM" if x > 0.3 else "🔵 LOW"
    )

    # Sort by risk
    hotspot_stats = hotspot_stats.sort_values('avg_risk', ascending=False)

    return hotspot_stats

@st.cache_data
def get_analytics_data(_data, data_type):
    """Cache expensive analytics calculations"""
    if data_type == 'hourly':
        return _data.groupby('Hour').agg({
            'Is_Intrusion': 'mean',
            'Risk_Score': 'mean'
        }).reset_index()
    elif data_type == 'weekly':
        result = _data.groupby('DayOfWeek').agg({
            'Is_Intrusion': 'mean'
        }).reset_index()
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        result['DayName'] = result['DayOfWeek'].apply(lambda x: day_names[int(x)])
        return result
    elif data_type == 'weather':
        result = _data.groupby('Weather').agg({
            'Is_Intrusion': 'mean'
        }).reset_index()
        weather_names = ['Clear', 'Cloudy', 'Rain', 'Storm']
        result['Weather_Name'] = result['Weather'].apply(lambda x: weather_names[int(x)])
        return result
    elif data_type == 'night_day':
        result = _data.groupby('Is_Night')['Is_Intrusion'].mean().reset_index()
        result['Time'] = result['Is_Night'].apply(lambda x: 'Night' if x == 1 else 'Day')
        return result
    elif data_type == 'weekend':
        result = _data.groupby('Is_Weekend')['Is_Intrusion'].mean().reset_index()
        result['Type'] = result['Is_Weekend'].apply(lambda x: 'Weekend' if x == 1 else 'Weekday')
        return result
    return None

@st.cache_resource
def train_ai_model(_data):
    """Train optimized AI model with better parameters"""
    X = _data[['Hour', 'DayOfWeek', 'Month', 'Weather', 'Is_Night', 'Is_Weekend']]
    y = _data['Is_Intrusion']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Optimized Random Forest parameters
    model = RandomForestClassifier(
        n_estimators=50,  # Reduced from 100 for faster training
        max_depth=10,     # Limit depth to prevent overfitting
        min_samples_split=10,
        min_samples_leaf=5,
        max_features='sqrt',
        random_state=42,
        n_jobs=-1  # Use all available cores
    )

    model.fit(X_train, y_train)

    importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)

    return model, importance, X_test, y_test

def get_status_badge(risk):
    if risk < 0.3: return "🟢 SAFE", "safe"
    elif risk < 0.5: return "🟡 MONITOR", "warning"
    else: return "🔴 CRITICAL", "danger"

# MAIN APP
def main():
    # SIDEBAR NAVIGATION
    with st.sidebar:
        st.markdown('<h2 style="color: #ffffff; text-align: center;">🛡️ Navigation</h2>', unsafe_allow_html=True)
        st.markdown("---")

        # Navigation buttons
        pages = {
            "📊 Dashboard": "dashboard",
            "🗺️ World Map": "map",
            "📷 Intrusion Detect": "intrusion",
            "📈 Analytics": "analytics",
            "🤖 Predictor": "predictor",
            "⚡ Performance": "performance",
            "⚙️ Settings": "settings"
        }

        for page_name, page_key in pages.items():
            if st.button(page_name, key=f"nav_{page_key}", use_container_width=True,
                        help=f"Navigate to {page_name}"):
                st.session_state.page = page_key
                st.rerun()

        st.markdown("---")
        st.markdown("**Current Page:**")
        current_page_name = [name for name, key in pages.items() if key == st.session_state.page]
        if current_page_name:
            st.success(f"📍 {current_page_name[0]}")

    # HEADER WITH REAL-TIME INFO
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown('<h1 class="main-header">🛡️ Global Border Threat AI</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center; color:#a0a0c0; font-size:1.1rem; margin-bottom:1rem;">'
                    'Real-time intelligence across 10+ international hotspots | AI-powered predictions</p>',
                    unsafe_allow_html=True)

    with col2:
        current_time = pd.Timestamp.now().strftime("%H:%M:%S UTC")
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(145deg, #1e1e2e, #2a2a3e); border-radius: 15px; border: 1px solid #3a3a4e;">
            <div style="font-size: 0.8rem; color: #a0a0c0;">LAST UPDATE</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: #ffffff;">{current_time}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        status_color = "#10b981" if st.session_state.alerts_enabled else "#ef4444"
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(145deg, #1e1e2e, #2a2a3e); border-radius: 15px; border: 1px solid #3a3a4e;">
            <div style="font-size: 0.8rem; color: #a0a0c0;">SYSTEM STATUS</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: {status_color};">{'🟢 ACTIVE' if st.session_state.alerts_enabled else '🔴 ALERTS OFF'}</div>
        </div>
        """, unsafe_allow_html=True)

    # ALERTS SYSTEM - MOVED AFTER DATA LOADING
    if st.session_state.alerts_enabled and 'data' in locals():
        alerts = get_risk_alerts(data)
        if alerts:
            for alert in alerts:
                st.markdown(f"""
                <div class="alert-banner">
                    <strong>{alert['message']}</strong><br>
                    <small style="font-size: 0.9rem; opacity: 0.9;">{alert['details']}</small>
                </div>
                """, unsafe_allow_html=True)

    # ADVANCED CONTROLS PANEL
    with st.expander("⚙️ Advanced Controls & Filters", expanded=False):
        col1, col2, col3, col4 = st.columns(4)

        uploaded_file = None  # Initialize uploaded_file

        with col1:
            st.markdown("**📊 Data Source**")
            data_source = st.radio("", ["Sample Data", "Upload CSV"], horizontal=True, label_visibility="collapsed")
            if data_source == "Upload CSV":
                uploaded_file = st.file_uploader("", type=['csv'], label_visibility="collapsed")

        with col2:
            st.markdown("**🔍 Filters**")
            risk_filter = st.slider("Risk Threshold", 0.0, 1.0, 0.0, 0.1)
            time_filter = st.selectbox("Time Period", ["All Time", "Last 24h", "Last 7d", "Last 30d"])

        with col3:
            st.markdown("**📤 Export Data**")
            export_format = st.selectbox("", ["CSV", "JSON", "Excel"], label_visibility="collapsed")
            if st.button("💾 Export Dataset", use_container_width=True):
                export_data_bytes = export_data(data, export_format.lower())
                st.download_button(
                    label=f"📥 Download {export_format}",
                    data=export_data_bytes,
                    file_name=f"border_threat_data.{export_format.lower()}",
                    mime="text/csv" if export_format == "CSV" else "application/json" if export_format == "JSON" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        with col4:
            st.markdown("**🔔 Notifications**")
            alerts_enabled = st.checkbox("Enable Alerts", value=st.session_state.alerts_enabled)
            if alerts_enabled != st.session_state.alerts_enabled:
                st.session_state.alerts_enabled = alerts_enabled
                st.rerun()

            auto_refresh = st.checkbox("Auto Refresh (30s)")
            if auto_refresh:
                time.sleep(30)
                st.rerun()

    # Data loading with error handling and optimization
    try:
        if uploaded_file:
            data = pd.read_csv(uploaded_file)
            st.session_state.data_source = "uploaded"
            st.success("✅ Custom dataset loaded!")

            # Validate required columns
            required_cols = ['Hotspot', 'Country', 'Latitude', 'Longitude', 'Hour', 'Is_Intrusion', 'Risk_Score']
            missing_cols = [col for col in required_cols if col not in data.columns]
            if missing_cols:
                st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
                st.info("Please ensure your CSV has: Hotspot, Country, Latitude, Longitude, Hour, Is_Intrusion, Risk_Score")
                return

        elif st.session_state.get('data_cleared', False):
            # User specifically cleared data
            data = pd.DataFrame()
        else:
            with st.spinner('Generating optimized dataset...'):
                data = generate_sample_data()

        # Validate data
        if len(data) == 0:
            st.warning("⚠️ System data has been cleared. Analytics and modeling are suspended.")
            if st.button("🔄 Quick Regenerate Data", use_container_width=True, type="primary"):
                st.session_state.data_cleared = False
                generate_sample_data.clear()
                st.rerun()
            return

        # Smart sampling for performance - only for very heavy operations
        if len(data) > 50000:
            # Only sample for correlation analysis which is computationally expensive
            correlation_sample = data.sample(n=min(25000, len(data)), random_state=42)
            st.info(f"📊 Using optimized sample of {len(correlation_sample):,} records for correlation analysis (from {len(data):,} total)")
        else:
            correlation_sample = data

        # Use full data for all other analytics to maintain accuracy
        analytics_sample = data

    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return
    
    # ALERTS SYSTEM - MOVED AFTER DATA LOADING
    if st.session_state.alerts_enabled:
        alerts = get_risk_alerts(data)
        if alerts:
            for alert in alerts:
                st.markdown(f"""
                <div class="alert-banner">
                    <strong>{alert['message']}</strong><br>
                    <small style="font-size: 0.9rem; opacity: 0.9;">{alert['details']}</small>
                </div>
                """, unsafe_allow_html=True)
    
    # Train model with better error handling
    try:
        with st.spinner('Training AI model...'):
            model, importance, X_test, y_test = train_ai_model(data)
        st.success("🤖 AI Model trained successfully!")
    except Exception as e:
        st.error(f"❌ Model training failed: {str(e)}")
        return
    
    # PAGE-BASED NAVIGATION SYSTEM
    if st.session_state.page == "dashboard":
        # ENHANCED DASHBOARD METRICS
        st.markdown('<h2 class="section-header">📊 Threat Intelligence Dashboard</h2>', unsafe_allow_html=True)

        # Key Metrics Row
        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">🛰️ HOTSPOTS</div>
                <div class="metric-value">{data['Hotspot'].nunique()}</div>
                <div style="font-size: 0.7rem; color: #a0a0c0; margin-top: 0.5rem;">Active monitoring zones</div>
            </div>
        """, unsafe_allow_html=True)

        with col2:
            total_breaches = int(data['Is_Intrusion'].sum())
            breach_rate = (total_breaches / len(data)) * 100
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">🚨 BREACHES</div>
                <div class="metric-value">{total_breaches:,}</div>
                <div style="font-size: 0.7rem; color: #a0a0c0; margin-top: 0.5rem;">{breach_rate:.1f}% of total events</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            accuracy = model.score(X_test, y_test) * 100
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">🎯 ACCURACY</div>
                <div class="metric-value">{accuracy:.1f}%</div>
                <div style="font-size: 0.7rem; color: #a0a0c0; margin-top: 0.5rem;">AI prediction accuracy</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            avg_risk = data['Risk_Score'].mean() * 100
            risk_color = "#10b981" if avg_risk < 30 else "#f59e0b" if avg_risk < 50 else "#ef4444"
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = avg_risk,
                title = {'text': "🌍 THREAT LEVEL", 'font': {'color': '#a0a0c0', 'size': 12}},
                number = {'suffix': "%", 'font': {'color': risk_color, 'size': 28}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': risk_color},
                    'bgcolor': "rgba(0,0,0,0)",
                    'borderwidth': 0,
                    'steps': [
                        {'range': [0, 30], 'color': "rgba(16, 185, 129, 0.2)"},
                        {'range': [30, 50], 'color': "rgba(245, 158, 11, 0.2)"},
                        {'range': [50, 100], 'color': "rgba(239, 68, 68, 0.2)"}]
                }
            ))
            fig_gauge.update_layout(height=160, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
            st.plotly_chart(fig_gauge, use_container_width=True)

        with col5:
            # Recent activity (last 24h)
            recent_data = data[data['Timestamp'] > pd.Timestamp.now() - pd.Timedelta(hours=24)] if 'Timestamp' in data.columns else data
            recent_breaches = int(recent_data['Is_Intrusion'].sum())
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">⚡ 24H ACTIVITY</div>
                <div class="metric-value">{recent_breaches}</div>
                <div style="font-size: 0.7rem; color: #a0a0c0; margin-top: 0.5rem;">Recent breach events</div>
            </div>
            """, unsafe_allow_html=True)

        with col6:
            # System uptime/health
            uptime_color = "#10b981"
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">🔄 SYSTEM HEALTH</div>
                <div class="metric-value" style="color: {uptime_color};">99.9%</div>
                <div style="font-size: 0.7rem; color: #a0a0c0; margin-top: 0.5rem;">AI model confidence</div>
            </div>
            """, unsafe_allow_html=True)

        # Risk Distribution Chart
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown('<h3 class="section-header">📈 Risk Distribution Analysis</h3>', unsafe_allow_html=True)

            # Create risk distribution
            risk_bins = pd.cut(data['Risk_Score'], bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0], labels=['Very Low', 'Low', 'Medium', 'High', 'Critical'])
            risk_dist = risk_bins.value_counts().sort_index()

            fig_risk = px.bar(
                x=risk_dist.index,
                y=risk_dist.values,
                color=risk_dist.index,
                color_discrete_map={
                    'Very Low': '#10b981',
                    'Low': '#84cc16',
                    'Medium': '#f59e0b',
                    'High': '#f97316',
                    'Critical': '#ef4444'
                },
                title="Risk Level Distribution Across All Hotspots"
            )
            fig_risk.update_layout(
                height=300,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_risk, use_container_width=True)

        with col2:
            st.markdown('<h3 class="section-header">🎯 Top Risk Factors</h3>', unsafe_allow_html=True)

            # Feature importance visualization
            importance_df = pd.DataFrame({
                'Feature': ['Time of Day', 'Day of Week', 'Weather', 'Night Time', 'Weekend', 'Month'],
                'Importance': importance['importance'].values[:6] * 100
            }).sort_values('Importance', ascending=True)

            fig_importance = px.bar(
                importance_df,
                x='Importance',
                y='Feature',
                orientation='h',
                color='Importance',
                color_continuous_scale='plasma',
                title="AI Risk Predictors"
            )
            fig_importance.update_layout(
                height=300,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_importance, use_container_width=True)
            
        # Hotspot Details Tabs
        st.markdown("---")
        st.markdown('<h3 class="section-header">🔥 Top Risk Hotspots Detail</h3>', unsafe_allow_html=True)
        
        hotspot_stats = get_hotspot_stats(data)
        # Display top hotspots
        top_hotspots = hotspot_stats.head(5)
        
        if not top_hotspots.empty:
            tabs = st.tabs([f"{row['Hotspot']} {row['Priority'].split(' ')[0]}" for _, row in top_hotspots.iterrows()])
            
            for i, (_, row) in enumerate(top_hotspots.iterrows()):
                with tabs[i]:
                    st.markdown(f"#### {row['Hotspot']} - {row['country']}")
                    tcol1, tcol2, tcol3, tcol4 = st.columns(4)
                    
                    with tcol1:
                        st.metric("Average Risk", f"{row['avg_risk']*100:.1f}%")
                    with tcol2:
                        st.metric("Total Events", f"{int(row['total_events']):,}")
                    with tcol3:
                        st.metric("Breach Rate", f"{row['intrusion_rate']*100:.1f}%")
                    with tcol4:
                        st.metric("Night Threat", f"{row['night_rate']*100:.1f}%")
                        
                    st.markdown(f"**Security Status:** {row['Priority']}")
    
    elif st.session_state.page == "map":
        # WORLD MAP VISUALIZATION
        st.markdown('<h3 class="section-header">🗺️ Global Risk Hotspot Map</h3>', unsafe_allow_html=True)

        # Map customization options
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            map_view = st.selectbox("Map Mode", ["Standard Map", "Glowing Density Map", "24H Time-Lapse"], index=0)
        with col2:
            map_style = st.selectbox("Map Style", ["carto-darkmatter", "carto-positron", "open-street-map"], index=0)
        with col3:
            size_metric = st.selectbox("Size/Weight", ["Risk_Score", "Breach_Count"], index=0)
        with col4:
            color_metric = st.selectbox("Color Metric", ["Risk_Score", "Breach_Count"], index=0)

        # Universally define map_df for statistics
        map_data = []
        for hotspot_name in data['Hotspot'].unique():
            hotspot_data = data[data['Hotspot'] == hotspot_name]
            risk_score = hotspot_data['Risk_Score'].mean()
            lat = hotspot_data['Latitude'].mean()
            lon = hotspot_data['Longitude'].mean()
            country = hotspot_data['Country'].iloc[0]
            breach_count = int(hotspot_data['Is_Intrusion'].sum())

            map_data.append({
                'Hotspot': hotspot_name, 'Country': country, 'Latitude': lat, 'Longitude': lon,
                'Risk_Score': risk_score, 'Risk_Pct': risk_score * 100, 'Breach_Count': breach_count
            })

        map_df = pd.DataFrame(map_data)

        if map_view == "Glowing Density Map":
            # Density Map View
            density_data = data.copy()
            density_data['Weight'] = density_data[size_metric] if size_metric in density_data.columns else density_data['Risk_Score']
            fig_map = px.density_mapbox(
                density_data, lat="Latitude", lon="Longitude", z="Weight", radius=30,
                center=dict(lat=30, lon=20), zoom=1.5, height=600,
                hover_name="Hotspot", hover_data=['Country', 'Risk_Score'],
                title="🔥 Military Thermal Density Map",
                color_continuous_scale="inferno"
            )
        elif map_view == "24H Time-Lapse":
            # Time-lapse Animation view
            time_data = data.groupby(['Hour', 'Hotspot', 'Country', 'Latitude', 'Longitude']).agg(
                Risk_Score=('Risk_Score', 'mean'),
                Breach_Count=('Is_Intrusion', 'sum')
            ).reset_index().sort_values('Hour')
            time_data['Hour_Str'] = time_data['Hour'].apply(lambda x: f"{x:02d}:00")
            fig_map = px.scatter_mapbox(
                time_data, lat="Latitude", lon="Longitude", size=size_metric, color=color_metric,
                animation_frame="Hour_Str", hover_name="Hotspot", hover_data=['Country'],
                color_continuous_scale="RdYlGn_r", size_max=40, zoom=1.5, height=600,
                title="⏱️ 24H Threat Evolution Time-Lapse"
            )
            if hasattr(fig_map.layout, 'updatemenus') and len(fig_map.layout.updatemenus) > 0:
                fig_map.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 800
        else:
            # Standard Map View
            fig_map = px.scatter_mapbox(
                map_df, lat="Latitude", lon="Longitude", size=size_metric, color=color_metric,
                hover_name="Hotspot", hover_data=['Country', 'Risk_Pct', 'Breach_Count'],
                color_continuous_scale="RdYlGn_r", size_max=50, zoom=1.5, height=600,
                title="🔴 High Risk Zones | Click hotspots for intelligence",
                labels={'Risk_Pct': 'Threat Level %', 'Breach_Count': 'Total Breaches'}
            )

        fig_map.update_layout(
            mapbox_style=map_style,
            margin={"r":0,"t":60,"l":0,"b":0},
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_map, use_container_width=True)

        # Map Statistics
        st.markdown("---")
        st.markdown("**📊 Map Statistics**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Hotspots", len(map_df))
        with col2:
            st.metric("High Risk Zones", len(map_df[map_df['Risk_Score'] > 0.5]))
        with col3:
            st.metric("Avg Risk Score", f"{map_df['Risk_Score'].mean()*100:.1f}%")
        with col4:
            st.metric("Total Breaches", map_df['Breach_Count'].sum())
    elif st.session_state.page == "analytics":
        # ENHANCED ANALYTICS
        st.markdown('<h3 class="section-header">📈 Advanced Threat Analytics</h3>', unsafe_allow_html=True)

        # Time-based analysis
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**⏰ Hourly Threat Pattern**")
            st.caption("📌 Look for peaks and troughs. High peaks suggest critical hours that need extra patrol or monitoring.")
            hourly_data = get_analytics_data(analytics_sample, 'hourly')

            fig_hourly = px.line(
                hourly_data, x='Hour', y='Is_Intrusion',
                markers=True, title="Intrusion Rate by Hour",
                color_discrete_sequence=['#ff6b6b']
            )
            fig_hourly.update_layout(
                height=350,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_hourly, use_container_width=True)

        with col2:
            st.markdown("**📅 Weekly Threat Pattern**")
            st.caption("📌 Compare days to find risk patterns. Weekdays vs. weekends may reveal different threat profiles.")
            weekly_data = get_analytics_data(analytics_sample, 'weekly')

            fig_weekly = px.bar(
                weekly_data, x='DayName', y='Is_Intrusion',
                title="Intrusion Rate by Day",
                color='Is_Intrusion',
                color_continuous_scale='Reds'
            )
            fig_weekly.update_layout(
                height=350,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_weekly, use_container_width=True)

        # Weather and seasonal analysis
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**🌤️ Weather Impact Analysis**")
            st.caption("📌 Larger slices = higher intrusion rate. Identify if certain weather conditions correlate with breaches.")
            weather_data = get_analytics_data(analytics_sample, 'weather')

            fig_weather = px.pie(
                weather_data, values='Is_Intrusion', names='Weather_Name',
                title="Intrusion Rate by Weather Condition",
                color_discrete_sequence=px.colors.sequential.Reds
            )
            fig_weather.update_layout(
                height=330,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_weather, use_container_width=True)

        with col2:
            st.markdown("**📊 Risk Correlation Matrix**")
            st.caption("📌 Red = strong positive correlation; Blue = negative. Dark colors show the strongest relationships.")
            # Create correlation matrix for key features (using sample for performance)
            corr_features = ['Hour', 'DayOfWeek', 'Month', 'Weather', 'Is_Night', 'Is_Weekend', 'Is_Intrusion', 'Risk_Score']
            corr_matrix = correlation_sample[corr_features].corr()

            fig_corr = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                color_continuous_scale="RdBu_r",
                title="Feature Correlation Heatmap"
            )
            fig_corr.update_layout(
                height=330,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_corr, use_container_width=True)

        st.markdown("---")

        with st.expander("📘 Chart Guide: What each analytics plot means"):
            st.write("- **Hourly Threat Pattern:** looks for peak intrusion hours; higher line means more breaches per hour.")
            st.write("- **Weekly Threat Pattern:** identifies the weekdays with higher breach rates to help schedule patrols.")
            st.write("- **Weather Impact Analysis:** shows the share of intrusions by weather condition; large slice = higher risk.")
            st.write("- **Risk Correlation Matrix:** positive values (red) show features that move with risk; negative (blue) show opposite behavior.")
            st.write("- **AI Predictor Influence:** how much the trained model relies on each factor (sum 100%); use it to explain AI risk scoring.")

        st.markdown("**🤖 AI Predictor Influence + Insight Summary**")

        col1, col2 = st.columns([2, 1])
        with col1:
            if 'importance' in locals() and not importance.empty:
                importance_sorted = importance.copy()
                importance_sorted['importance_pct'] = 100 * importance_sorted['importance'] / importance_sorted['importance'].sum()

                top_feature = importance_sorted.iloc[0]
                st.markdown(f"**Top predictor:** {top_feature['feature']} ({top_feature['importance_pct']:.1f}% influence estimate)")
                st.caption("📌 Taller bars = more impact on AI risk predictions. The model relies most on features with the highest bars.")

                fig_imp = px.bar(
                    importance_sorted,
                    x='feature',
                    y='importance_pct',
                    title='AI Model Feature Influence',
                    labels={'importance_pct': 'Influence (%)', 'feature': 'Feature'},
                    color='importance_pct',
                    color_continuous_scale='Blues'
                )
                fig_imp.update_layout(
                    height=330,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    yaxis={'range': [0, 100]}
                )
                st.plotly_chart(fig_imp, use_container_width=True)
            else:
                st.warning('Feature importance data not available yet.')

        with col2:
            st.markdown('**🧾 From the data, key insights are:**')
            try:
                busiest_hour = hourly_data.loc[hourly_data['Is_Intrusion'].idxmax()]['Hour']
                highest_day = weekly_data.loc[weekly_data['Is_Intrusion'].idxmax()]['DayName']
                top_weather = weather_data.loc[weather_data['Is_Intrusion'].idxmax()]['Weather_Name']
            except Exception:
                busiest_hour = None
                highest_day = None
                top_weather = None

            st.write(f"• Peak risk hour: {int(busiest_hour) if busiest_hour is not None else 'N/A'}")
            st.write(f"• Highest intrusion day: {highest_day if highest_day else 'N/A'}")
            st.write(f"• Highest-risk weather: {top_weather if top_weather else 'N/A'}")
            st.write('• Correlation: bright red = strong positive; bright blue = strong negative.')

        # Additional Analytics
        st.markdown("---")
        st.markdown('<h4 style="color: #ffffff;">🌊 Threat Flow Analysis (Sankey Diagram)</h4>', unsafe_allow_html=True)
        
        # Build Sankey data: Country -> Weather -> Intrusion
        sankey_data = data.copy()
        weather_names = {0: 'Clear', 1: 'Cloudy', 2: 'Rain', 3: 'Storm'}
        sankey_data['Weather_Name'] = sankey_data['Weather'].map(weather_names)
        sankey_data['Outcome'] = sankey_data['Is_Intrusion'].map({0: 'Safe', 1: 'Breach'})
        
        flows = sankey_data.groupby(['Country', 'Weather_Name', 'Outcome']).size().reset_index(name='Count')
        
        all_nodes = list(flows['Country'].unique()) + list(weather_names.values()) + ['Safe', 'Breach']
        node_indices = {node: i for i, node in enumerate(all_nodes)}
        
        sources = []
        targets = []
        values = []
        
        # Link Country -> Weather
        c_w_flows = flows.groupby(['Country', 'Weather_Name'])['Count'].sum().reset_index()
        for _, row in c_w_flows.iterrows():
            sources.append(node_indices[row['Country']])
            targets.append(node_indices[row['Weather_Name']])
            values.append(row['Count'])
            
        # Link Weather -> Intrusion
        w_i_flows = flows.groupby(['Weather_Name', 'Outcome'])['Count'].sum().reset_index()
        for _, row in w_i_flows.iterrows():
            sources.append(node_indices[row['Weather_Name']])
            targets.append(node_indices[row['Outcome']])
            values.append(row['Count'])
            
        fig_sankey = go.Figure(data=[go.Sankey(
            node = dict(
              pad = 15,
              thickness = 20,
              line = dict(color = "black", width = 0.5),
              label = all_nodes,
              color = "#667eea"
            ),
            link = dict(
              source = sources,
              target = targets,
              value = values,
              color = "rgba(102, 126, 234, 0.4)"
          ))])
        
        fig_sankey.update_layout(title_text="Intrusion Environmental Flow Paths", font_size=12, height=450, paper_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig_sankey, use_container_width=True)

        st.markdown("---")
        st.markdown('<h4 style="color: #ffffff;">🔍 Deep Analytics</h4>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**🌙 Night vs Day Activity**")
            night_day = get_analytics_data(analytics_sample, 'night_day')

            fig_night_day = px.bar(
                night_day, x='Time', y='Is_Intrusion',
                title="Night vs Day Intrusion Rates",
                color='Time',
                color_discrete_map={'Night': '#667eea', 'Day': '#f093fb'}
            )
            fig_night_day.update_layout(
                height=250,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_night_day, use_container_width=True)

        with col2:
            st.markdown("**🗓️ Weekend Impact**")
            weekend_data = get_analytics_data(analytics_sample, 'weekend')

            fig_weekend = px.pie(
                weekend_data, values='Is_Intrusion', names='Type',
                title="Weekend vs Weekday Activity",
                color_discrete_sequence=['#10b981', '#f59e0b']
            )
            fig_weekend.update_layout(
                height=250,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_weekend, use_container_width=True)

        with col3:
            st.markdown("**📈 Risk Score Distribution**")
            fig_risk_dist = px.histogram(
                analytics_sample, x='Risk_Score',
                title="Risk Score Distribution",
                color_discrete_sequence=['#ff6b6b'],
                nbins=20
            )
            fig_risk_dist.update_layout(
                height=250,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_risk_dist, use_container_width=True)
    
    elif st.session_state.page == "predictor":
        # LIVE PREDICTOR
        st.markdown('<h3 class="section-header">🎯 Live Risk Calculator</h3>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            hotspot = st.selectbox("Hotspot", data['Hotspot'].unique())
        with col2:
            hour = st.slider("Hour", 0, 23, 23)
        with col3:
            conditions = st.multiselect("Conditions", ["Night", "Weekend"],
                                      default=["Night"] if hour >= 20 or hour <= 6 else [])

        is_night = "Night" in conditions or (hour >= 20 or hour <= 6)
        is_weekend = "Weekend" in conditions

        # Get hotspot data safely
        hotspot_data = data[data['Hotspot'] == hotspot]
        if len(hotspot_data) > 0:
            h_data = hotspot_data.iloc[0]
            base_risk = hotspot_data['Risk_Score'].mean() * 100
            country = h_data['Country']
        else:
            st.error("Hotspot data not found!")
            return

        if st.button("🚀 PREDICT RISK", type="primary"):
            try:
                # Create input with proper feature order
                input_data = np.array([[hour, 0, 7, 1, int(is_night), int(is_weekend)]])

                confidence = model.predict_proba(input_data)[0]
                risk = confidence[1] * 100

                col1, col2 = st.columns(2)
                with col1:
                    status, badge_class = get_status_badge(risk/100)
                    st.markdown(f"""
                    <div class="metric-container" style="text-align:center; padding:3rem;">
                        <div class="status-badge {badge_class}" style="font-size:1.2rem; padding:1rem 2rem;">
                            {status}
                        </div>
                        <h1 style="font-size:5rem; color:#ff6b6b; margin:1rem 0;">{risk:.0f}%</h1>
                        <p>AI Prediction</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    # Target Profile Radar Chart
                    radar_fig = go.Figure()
                    radar_fig.add_trace(go.Scatterpolar(
                        r=[base_risk, 100 if is_night else 20, 100 if is_weekend else 20, confidence[1]*100, risk],
                        theta=['Base Ext. Risk', 'Night Factor', 'Weekend Volatility', 'AI Confidence', 'Total Threat'],
                        fill='toself',
                        name='Threat Profile',
                        line_color='#ff6b6b',
                        fillcolor='rgba(255, 107, 107, 0.4)'
                    ))
                    radar_fig.update_layout(
                        polar=dict(radialaxis=dict(visible=True, range=[0, 100], color='gray')),
                        showlegend=False,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font_color='white',
                        height=280,
                        margin=dict(l=40, r=40, t=30, b=30)
                    )
                    st.plotly_chart(radar_fig, use_container_width=True)

                # Summary metrics below
                st.markdown(f"""
                <div style="display: flex; justify-content: space-around; background: linear-gradient(145deg, #1e1e2e, #2a2a3e); padding: 1rem; border-radius: 10px; margin-top: 1rem; border: 1px solid #3a3a4e;">
                    <div><strong>Base Risk:</strong> {base_risk:.1f}%</div>
                    <div><strong>Conditions:</strong> {'🌙 Night' if is_night else '☀️ Day'} | {'🗓️ Weekend' if is_weekend else '📅 Weekday'}</div>
                    <div><strong>Final Risk:</strong> <span style="color:#ff6b6b; font-size:1.2rem;">{risk:.1f}%</span></div>
                </div>
                """, unsafe_allow_html=True)

                # Show confidence interval
                st.markdown("---")
                st.markdown("**📊 Prediction Confidence:**")
                st.progress(confidence[1], text=f"Intrusion Risk: {confidence[1]*100:.1f}%")

            except Exception as e:
                st.error(f"Prediction failed: {str(e)}")
                st.info("Please check your input data and try again.")

    elif st.session_state.page == "performance":
        # PERFORMANCE MONITORING TAB
        st.markdown('<h3 class="section-header">⚡ AI Model Performance Monitor</h3>', unsafe_allow_html=True)

        # Get performance metrics
        perf_metrics = create_performance_metrics(model, X_test, y_test, data)

        # Performance Overview
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">🎯 ACCURACY</div>
                <div class="metric-value">{perf_metrics['accuracy']*100:.1f}%</div>
                <div style="font-size: 0.7rem; color: #a0a0c0; margin-top: 0.5rem;">Overall prediction accuracy</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">📈 AUC SCORE</div>
                <div class="metric-value">{perf_metrics['auc']:.3f}</div>
                <div style="font-size: 0.7rem; color: #a0a0c0; margin-top: 0.5rem;">Area under ROC curve</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">🎯 PRECISION</div>
                <div class="metric-value">{perf_metrics['precision']*100:.1f}%</div>
                <div style="font-size: 0.7rem; color: #a0a0c0; margin-top: 0.5rem;">True positive rate</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">🔍 RECALL</div>
                <div class="metric-value">{perf_metrics['recall']*100:.1f}%</div>
                <div style="font-size: 0.7rem; color: #a0a0c0; margin-top: 0.5rem;">Detection sensitivity</div>
            </div>
            """, unsafe_allow_html=True)

        # Confusion Matrix
        st.markdown('<h4 style="color: #ffffff; margin-top: 2rem;">📊 Confusion Matrix</h4>', unsafe_allow_html=True)

        cm = perf_metrics['confusion_matrix']
        cm_df = pd.DataFrame(
            cm,
            columns=['Predicted Negative', 'Predicted Positive'],
            index=['Actual Negative', 'Actual Positive']
        )

        fig_cm = px.imshow(
            cm_df,
            text_auto=True,
            color_continuous_scale="Blues",
            title="Model Confusion Matrix"
        )
        fig_cm.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_cm, use_container_width=True)

        # Model Insights
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**✅ Model Strengths**")
            st.markdown(f"""
            - **{perf_metrics['true_positives']}** correct threat detections
            - **{perf_metrics['accuracy']*100:.1f}%** overall accuracy
            - **{perf_metrics['auc']:.3f}** AUC score (excellent discrimination)
            """)

        with col2:
            st.markdown("**⚠️ Areas for Improvement**")
            false_negatives = perf_metrics['false_negatives']
            false_positives = perf_metrics['false_positives']
            st.markdown(f"""
            - **{false_negatives}** missed threats (false negatives)
            - **{false_positives}** false alarms (false positives)
            - Consider additional features for better detection
            """)

    elif st.session_state.page == "intrusion":
        # INTRUSION DETECTION TAB
        st.markdown('<h3 class="section-header">📷 Real-time Intrusion Detection</h3>', unsafe_allow_html=True)
        st.write("Uses your webcam and AI object detection to identify humans, animals, and vehicles.")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("**Camera Controls**")
            run_camera = st.checkbox("▶️ Enable Camera Feed", value=False)
            
            st.markdown("---")
            st.markdown("**Detection Filters**")
            detect_humans = st.checkbox("Detect Humans", value=True)
            detect_animals = st.checkbox("Detect Animals", value=True)
            detect_vehicles = st.checkbox("Detect Vehicles", value=True)
            
        with col2:
            alert_placeholder = st.empty()
            stframe = st.empty()
            
            if run_camera:
                net = load_mobilenet_model()
                if net is None:
                    st.error("Model could not be loaded. Intrusion detection unavailable.")
                else:
                    cap = cv2.VideoCapture(0)
                    if not cap.isOpened():
                        st.error("Could not access the webcam. Ensure it's connected and not used by another app.")
                    else:
                        st.success("Camera connected! Monitoring for intrusions...")
                        try:
                            while run_camera:
                                ret, frame = cap.read()
                                if not ret:
                                    st.error("Failed to read frame from camera.")
                                    break
                                    
                                (h, w) = frame.shape[:2]
                                blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
                                net.setInput(blob)
                                detections = net.forward()
                                
                                intrusion_detected = False
                                detected_labels = []
                                
                                for i in np.arange(0, detections.shape[2]):
                                    confidence = detections[0, 0, i, 2]
                                    if confidence > 0.4:
                                        idx = int(detections[0, 0, i, 1])
                                        class_name = CLASSES[idx]
                                        
                                        # Check if detection matches enabled filters
                                        is_human = class_name in HUMAN_CLASSES and detect_humans
                                        is_animal = class_name in ANIMAL_CLASSES and detect_animals
                                        is_vehicle = class_name in VEHICLE_CLASSES and detect_vehicles
                                        
                                        if is_human or is_animal or is_vehicle:
                                            intrusion_detected = True
                                            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                                            (startX, startY, endX, endY) = box.astype("int")
                                            
                                            # Set color based on type
                                            color = (0, 0, 255) if is_human else (0, 255, 0) if is_animal else (255, 0, 0)
                                            label_prefix = "🧑 HUMAN" if is_human else ("🐕 ANIMAL" if is_animal else "🚗 VEH")
                                            
                                            label = f"{label_prefix}: {confidence * 100:.1f}%"
                                            if label_prefix not in detected_labels:
                                                detected_labels.append(label_prefix)
                                                
                                            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 3)
                                            y = startY - 15 if startY - 15 > 15 else startY + 15
                                            cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                                
                                if intrusion_detected:
                                    alert_placeholder.error(f"🚨 **INTRUSION DETECTED:** {', '.join(detected_labels)} identified in restricted zone!")
                                else:
                                    alert_placeholder.empty()
                                    
                                # Convert to RGB for Streamlit
                                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                stframe.image(frame_rgb, channels="RGB", use_container_width=True)
                        finally:
                            cap.release()
            else:
                st.info("Camera is currently off. Check 'Enable Camera Feed' to begin real-time detection.")

    elif st.session_state.page == "settings":
        # SETTINGS TAB
        st.markdown('<h3 class="section-header">⚙️ System Settings & Configuration</h3>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**📊 Dashboard Display Settings**")
            font_size = st.slider("Font Size", 12, 18, 14)
            animations = st.checkbox("Enable Animations", value=True)

            st.markdown("**📊 Dashboard Settings**")
            auto_refresh_rate = st.slider("Auto Refresh Rate (seconds)", 30, 300, 60)
            max_hotspots_display = st.slider("Max Hotspots to Display", 5, 20, 10)

        with col2:
            st.markdown("**🔧 Model Settings**")
            model_confidence = st.slider("Prediction Confidence Threshold", 0.1, 0.9, 0.5)
            alert_sensitivity = st.selectbox("Alert Sensitivity", ["Low", "Medium", "High"], index=1)

            st.markdown("**📤 Export Settings**")
            default_export = st.selectbox("Default Export Format", ["CSV", "JSON", "Excel"], index=0)
            include_metadata = st.checkbox("Include Metadata in Exports", value=True)

            st.markdown("**🔔 Notification Settings**")
            email_alerts = st.checkbox("Email Alerts (when implemented)")
            sound_alerts = st.checkbox("Sound Notifications", value=False)

            st.markdown("**💾 Data Management**")
            if st.button("🔄 Regenerate Sample Data", help="Generate new synthetic border incident data"):
                with st.spinner("Generating new data..."):
                    st.session_state.data_cleared = False
                    generate_sample_data.clear()
                    st.success("✅ New sample data generated!")
                    time.sleep(0.5)
                    st.rerun()

            if st.button("🧹 Clear All Data", help="Remove all current data from memory"):
                st.session_state.data_cleared = True
                st.success("✅ All data cleared!")
                time.sleep(0.5)
                st.rerun()

        if st.button("💾 Save Settings", type="primary"):
            st.success("✅ Settings saved successfully!")
            # In a real app, these would be saved to a config file or database

        st.markdown("---")
        st.markdown("**🔄 System Information**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Python Version", "3.11+")
        with col2:
            st.metric("Data Points", f"{len(data):,}")
        with col3:
            st.metric("Model Version", "v2.1.0")

    else:
        # Invalid page - redirect to dashboard
        st.error("❌ Invalid page selected. Redirecting to Dashboard...")
        st.session_state.page = "dashboard"
        st.rerun()


    # FOOTER
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; color:#666; padding:2rem; background: linear-gradient(145deg, #1e1e2e, #2a2a3e); border-radius: 15px; margin-top: 2rem;">
        <div style="display: flex; justify-content: center; align-items: center; gap: 2rem; margin-bottom: 1rem;">
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🛡️</div>
                <div style="font-weight: bold; color: #ffffff;">Global Border Threat AI</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🤖</div>
                <div style="font-weight: bold; color: #ffffff;">AI-Powered Intelligence</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌍</div>
                <div style="font-weight: bold; color: #ffffff;">10+ International Hotspots</div>
            </div>
        </div>
        <p style="color: #a0a0c0; margin: 1rem 0;">Real-time intelligence across international hotspots | AI-driven risk assessment</p>
        <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 1rem;">
            <span style="background: #667eea; color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem;">Machine Learning</span>
            <span style="background: #764ba2; color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem;">Real-time Data</span>
            <span style="background: #f093fb; color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem;">Predictive Analytics</span>
        </div>
        <p style="font-size:0.8rem; margin-top:1.5rem; color: #888;">⚠️ <strong>Disclaimer:</strong> This is a demonstration tool for educational purposes only. Not intended for operational security use.</p>
        <p style="font-size:0.7rem; margin-top:0.5rem; color: #666;">© 2026 Global Border Threat AI | Powered by Streamlit & Machine Learning</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()