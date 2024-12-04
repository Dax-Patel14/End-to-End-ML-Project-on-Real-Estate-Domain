import streamlit as st

# Home Page Design
st.title("🏡 RealEase: Real Estate Price Prediction and Insights")
st.subheader("Make Informed Decisions in the Real Estate Market")

# About Section
st.markdown("""
Welcome to RealEase! This platform leverages advanced machine learning to:
- Predict property prices.
- Provide actionable market insights.
- Recommend properties tailored to your needs.
Explore our modules and empower your real estate journey!
""")

# Feature Overview
st.markdown("### 🌟 Key Features")
st.markdown("""
1. **Prediction Module**: Get accurate price predictions for your property.
2. **Analytics Module**: Visualize real estate market trends.
3. **Recommendation Module**: Discover personalized property recommendations.
4. **Insight Module**: Gain actionable insights for smarter decisions.
""")

# Call-to-Action Buttons
st.markdown("### Ready to dive in?")
col1, col2 = st.columns(2)
with col1:
    if st.button("🔮 Get Predictions"):
        st.write("Navigate to the Prediction Module!")
with col2:
    if st.button("📊 Explore Analytics"):
        st.write("Navigate to the Analytics Module!")

# Footer
st.markdown("---")
st.markdown("Powered by **Machine Learning** | © 2024 RealEase")
