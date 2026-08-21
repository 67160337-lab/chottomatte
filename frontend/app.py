import streamlit as st
import requests
import pandas as pd


# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Wastewater AI",
    page_icon="💧",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"


# =========================================================
# SESSION
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


# =========================================================
# GET USER ID
# =========================================================

def get_user_id():

    if not st.session_state.user:
        return None

    return st.session_state.user.get("user_id")


# =========================================================
# API REQUEST
# =========================================================

def api_request(method, endpoint, data=None):

    url = f"{API_URL}{endpoint}"

    try:

        response = requests.request(
            method=method,
            url=url,
            json=data,
            timeout=10
        )

        # พยายามอ่าน JSON
        try:

            result = response.json()

        except ValueError:

            result = {
                "error": response.text
                if response.text
                else "Backend did not return JSON"
            }

        # API Error
        if not response.ok:

            if isinstance(result, dict):

                return {
                    "error": result.get(
                        "detail",
                        result.get(
                            "message",
                            result.get(
                                "error",
                                f"HTTP {response.status_code}"
                            )
                        )
                    )
                }

            return {
                "error": f"HTTP {response.status_code}"
            }

        return result

    except requests.exceptions.ConnectionError:

        return {
            "error": (
                "ไม่สามารถเชื่อมต่อ Backend ได้ "
                "กรุณาตรวจสอบ FastAPI"
            )
        }

    except requests.exceptions.Timeout:

        return {
            "error": "Backend ใช้เวลาตอบกลับนานเกินไป"
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# =========================================================
# LOGIN / REGISTER PAGE
# =========================================================

def login_page():

    left, center, right = st.columns(
        [1, 2, 1]
    )

    with center:

        st.markdown(
            """
            <h1 style="text-align:center;">
                💧 Wastewater AI
            </h1>

            <p style="text-align:center;">
                ระบบติดตามคุณภาพน้ำ
                และคาดการณ์ความเร็ว Aerator ด้วย AI
            </p>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        tab_login, tab_register = st.tabs(
            [
                "🔐 Login",
                "📝 Register"
            ]
        )

        # =================================================
        # LOGIN
        # =================================================

        with tab_login:

            st.subheader("เข้าสู่ระบบ")

            username = st.text_input(
                "Username",
                key="login_username"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="login_password"
            )

            st.write("")

            if st.button(
                "Login",
                use_container_width=True
            ):

                if not username or not password:

                    st.warning(
                        "กรุณากรอก Username และ Password"
                    )

                else:

                    result = api_request(
                        "POST",
                        "/auth/login",
                        {
                            "username": username,
                            "password": password
                        }
                    )

                    if "error" in result:

                        st.error(
                            result["error"]
                        )

                    else:

                        st.session_state.logged_in = True

                        st.session_state.user = result

                        st.success(
                            "Login สำเร็จ"
                        )

                        st.rerun()

        # =================================================
        # REGISTER
        # =================================================

        with tab_register:

            st.subheader("สมัครสมาชิก")

            with st.form("register_form"):

                new_username = st.text_input(
                    "Username"
                )

                new_email = st.text_input(
                    "Email"
                )

                new_password = st.text_input(
                    "Password",
                    type="password"
                )

                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password"
                )

                register_submit = st.form_submit_button(
                    "Register",
                    use_container_width=True
                )

            # ---------------------------------------------
            # Register
            # ---------------------------------------------

            if register_submit:

                if not new_username.strip():

                    st.warning(
                        "กรุณากรอก Username"
                    )

                elif not new_email.strip():

                    st.warning(
                        "กรุณากรอก Email"
                    )

                elif not new_password:

                    st.warning(
                        "กรุณากรอก Password"
                    )

                elif not confirm_password:

                    st.warning(
                        "กรุณากรอก Confirm Password"
                    )

                elif new_password != confirm_password:

                    st.error(
                        "Password ไม่ตรงกัน"
                    )

                else:

                    result = api_request(
                        "POST",
                        "/auth/register",
                        {
                            "username": new_username.strip(),
                            "email": new_email.strip(),
                            "password": new_password
                        }
                    )

                    if "error" in result:

                        st.error(
                            result["error"]
                        )

                    else:

                        st.success(
                            "สมัครสมาชิกสำเร็จ! กรุณา Login"
                        )


# =========================================================
# DASHBOARD
# =========================================================

def dashboard():

    st.title("💧 Wastewater AI Dashboard")

    st.write(
        "ระบบติดตามคุณภาพน้ำ "
        "และคาดการณ์ความเร็ว Aerator ด้วย AI"
    )

    st.divider()

    user_id = get_user_id()

    if user_id is None:

        st.error(
            "ไม่พบ User ID กรุณา Login ใหม่"
        )

        return

    # =====================================================
    # GET WATER QUALITY
    # =====================================================

    latest_water = api_request(
        "GET",
        f"/water/latest?user_id={user_id}"
    )

    # =====================================================
    # GET AERATOR
    # =====================================================

    aerator = api_request(
        "GET",
        f"/aerator/?user_id={user_id}"
    )

    # =====================================================
    # WATER QUALITY
    # =====================================================

    st.subheader("🌊 Latest Water Quality")

    if (
        latest_water
        and "error" not in latest_water
        and "message" not in latest_water
    ):

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "DO",
                f"{latest_water.get('do', 0)} mg/L"
            )

        with col2:

            st.metric(
                "Temperature",
                f"{latest_water.get('temperature', 0)} °C"
            )

        with col3:

            st.metric(
                "Flow Rate",
                f"{latest_water.get('flow_rate', 0)}"
            )

        with col4:

            st.metric(
                "COD",
                f"{latest_water.get('cod', 0)} mg/L"
            )

    else:

        st.info(
            "ยังไม่มีข้อมูล Water Quality"
        )

    st.divider()

    # =====================================================
    # AERATOR
    # =====================================================

    st.subheader("⚙️ Aerator Status")

    if (
        aerator
        and "error" not in aerator
    ):

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Mode",
                aerator.get(
                    "mode",
                    "AUTO"
                )
            )

        with col2:

            st.metric(
                "Speed",
                f"{aerator.get('speed', 0)}%"
            )

    else:

        st.info(
            "ยังไม่มีข้อมูล Aerator"
        )


# =========================================================
# WATER QUALITY PAGE
# =========================================================

def water_quality_page():

    st.title("🌊 Water Quality")

    st.write(
        "บันทึกและตรวจสอบคุณภาพน้ำ"
    )

    st.divider()

    st.subheader("เพิ่มข้อมูล Water Quality")

    col1, col2 = st.columns(2)

    with col1:

        do = st.number_input(
            "DO (mg/L)",
            min_value=0.0,
            value=2.5
        )

        temperature = st.number_input(
            "Temperature (°C)",
            min_value=0.0,
            value=30.0
        )

    with col2:

        flow_rate = st.number_input(
            "Flow Rate",
            min_value=0.0,
            value=50.0
        )

        cod = st.number_input(
            "COD (mg/L)",
            min_value=0.0,
            value=300.0
        )

    status = st.selectbox(
        "Status",
        [
            "NORMAL",
            "WARNING",
            "CRITICAL"
        ]
    )

    # =====================================================
    # SAVE
    # =====================================================

    if st.button(
        "💾 Save Water Quality",
        use_container_width=True
    ):

        user_id = get_user_id()

        if user_id is None:

            st.error(
                "ไม่พบ User ID กรุณา Login ใหม่"
            )

        else:

            result = api_request(
                "POST",
                f"/water/?user_id={user_id}",
                {
                    "do": do,
                    "temperature": temperature,
                    "flow_rate": flow_rate,
                    "cod": cod,
                    "status": status
                }
            )

            if "error" in result:

                st.error(
                    result["error"]
                )

            else:

                st.success(
                    "บันทึกข้อมูลสำเร็จ"
                )

    st.divider()

    # =====================================================
    # HISTORY
    # =====================================================

    st.subheader(
        "📋 Water Quality History"
    )

    user_id = get_user_id()

    if user_id is None:

        st.info(
            "กรุณา Login"
        )

    else:

        history = api_request(
            "GET",
            f"/water/?user_id={user_id}"
        )

        if isinstance(history, list) and history:

            df = pd.DataFrame(history)

            st.dataframe(
                df,
                use_container_width=True
            )

        else:

            st.info(
                "ยังไม่มีข้อมูล"
            )


# =========================================================
# AI PREDICTION PAGE
# =========================================================

def ai_prediction_page():

    st.title("🤖 AI Prediction")

    st.write(
        "คาดการณ์ความเร็ว Aerator "
        "จากคุณภาพน้ำ"
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        influent_cod = st.number_input(
            "Influent COD",
            min_value=0.0,
            value=300.0
        )

        flow_rate = st.number_input(
            "Flow Rate",
            min_value=0.0,
            value=50.0
        )

    with col2:

        water_temp = st.number_input(
            "Water Temperature",
            min_value=0.0,
            value=30.0
        )

        current_do = st.number_input(
            "Current DO",
            min_value=0.0,
            value=2.5
        )

    st.write("")

    # =====================================================
    # PREDICT
    # =====================================================

    if st.button(
        "🤖 Predict Aerator Speed",
        use_container_width=True
    ):

        user_id = get_user_id()

        if user_id is None:

            st.error(
                "ไม่พบ User ID กรุณา Login ใหม่"
            )

        else:

            result = api_request(
                "POST",
                f"/ai/predict?user_id={user_id}",
                {
                    "influent_cod": influent_cod,
                    "flow_rate": flow_rate,
                    "water_temp": water_temp,
                    "current_do": current_do
                }
            )

            if "error" in result:

                st.error(
                    result["error"]
                )

            else:

                predicted_speed = result.get(
                    "predicted_speed",
                    0
                )

                st.success(
                    "AI Prediction สำเร็จ"
                )

                st.metric(
                    "Predicted Aerator Speed",
                    f"{predicted_speed:.2f}%"
                )


# =========================================================
# AERATOR CONTROL PAGE
# =========================================================

def aerator_page():

    st.title("⚙️ Aerator Control")

    user_id = get_user_id()

    if user_id is None:

        st.error(
            "ไม่พบ User ID กรุณา Login ใหม่"
        )

        return

    # =====================================================
    # GET CURRENT AERATOR
    # =====================================================

    current = api_request(
        "GET",
        f"/aerator/?user_id={user_id}"
    )

    if (
        current
        and "error" not in current
    ):

        st.info(
            f"Current Mode: "
            f"{current.get('mode', 'AUTO')} | "
            f"Speed: "
            f"{current.get('speed', 0)}%"
        )

    st.divider()

    # =====================================================
    # CONTROL
    # =====================================================

    mode = st.selectbox(
        "Mode",
        [
            "AUTO",
            "MANUAL"
        ]
    )

    speed = st.slider(
        "Aerator Speed (%)",
        min_value=0,
        max_value=100,
        value=50
    )

    if st.button(
        "⚙️ Update Aerator",
        use_container_width=True
    ):

        result = api_request(
            "PUT",
            f"/aerator/?user_id={user_id}",
            {
                "mode": mode,
                "speed": speed
            }
        )

        if "error" in result:

            st.error(
                result["error"]
            )

        else:

            st.success(
                "อัปเดต Aerator สำเร็จ"
            )

            st.rerun()


# =========================================================
# PREDICTION HISTORY PAGE
# =========================================================

def prediction_history_page():

    st.title("📊 Prediction History")

    st.write(
        "ประวัติการคาดการณ์ความเร็ว Aerator"
    )

    st.divider()

    user_id = get_user_id()

    if user_id is None:

        st.error(
            "ไม่พบ User ID กรุณา Login ใหม่"
        )

        return

    history = api_request(
        "GET",
        f"/ai/history?user_id={user_id}"
    )

    if isinstance(history, list) and history:

        df = pd.DataFrame(history)

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.info(
            "ยังไม่มีประวัติการ Prediction"
        )


# =========================================================
# MAIN PROGRAM
# =========================================================

# ---------------------------------------------------------
# ถ้ายังไม่ได้ Login
# ---------------------------------------------------------

if not st.session_state.logged_in:

    login_page()

    st.stop()


# =========================================================
# LOGIN แล้วจึงแสดงระบบ
# =========================================================

user = st.session_state.user

username = user.get(
    "username",
    "User"
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("💧 Wastewater AI")

    st.write(
        f"👤 **{username}**"
    )

    st.divider()

    page = st.radio(
        "Menu",
        [
            "Dashboard",
            "Water Quality",
            "AI Prediction",
            "Aerator Control",
            "Prediction History"
        ]
    )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False

        st.session_state.user = None

        st.rerun()


# =========================================================
# PAGE ROUTER
# =========================================================

if page == "Dashboard":

    dashboard()

elif page == "Water Quality":

    water_quality_page()

elif page == "AI Prediction":

    ai_prediction_page()

elif page == "Aerator Control":

    aerator_page()

elif page == "Prediction History":

    prediction_history_page()