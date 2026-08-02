import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="AI Emotion Analyzer", page_icon="🎭", layout="centered")

@st.cache_resource
def load_emotion_model():
    return pipeline(
        "text-classification", 
        model="bhadresh-savani/distilbert-base-uncased-emotion", 
        top_k=None
    )

classifier = load_emotion_model()

EMOJI_MAP = {
    "love": "❤️ Love",
    "anger": "🤬 Hate / Anger",
    "joy": "😄 Joy",
    "sadness": "😢 Sadness / Heartbreak",
    "fear": "😨 Fear",
    "surprise": "😲 Surprise"
}

st.title("🎭 Advanced AI Emotion Analyzer")

user_input = st.text_area(
    label="Enter Text to Analyze:",
    value="",
    placeholder="Type here...",
    height=150
)

if st.button("Analyze Emotion", type="primary"):
    if user_input.strip():
        with st.spinner("Analyzing context..."):
            results = classifier(user_input)[0]
            sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
            top_pred = sorted_results[0]

        st.markdown("---")
        st.subheader("Result")

        top_label = top_pred['label']
        display_label = EMOJI_MAP.get(top_label, top_label.capitalize())
        top_score = top_pred['score'] * 100

        if top_label in ["anger", "sadness", "fear"]:
            st.error(f"**Dominant Emotion:** {display_label} ({top_score:.1f}% Confidence)")
        elif top_label in ["love", "joy"]:
            st.success(f"**Dominant Emotion:** {display_label} ({top_score:.1f}% Confidence)")
        else:
            st.info(f"**Dominant Emotion:** {display_label} ({top_score:.1f}% Confidence)")

        st.write("### Detailed Emotion Breakdown")
        for item in sorted_results:
            label_name = EMOJI_MAP.get(item['label'], item['label'].capitalize())
            score_pct = item['score']
            st.write(f"**{label_name}** ({score_pct * 100:.1f}%)")
            st.progress(score_pct)
    else:
        st.warning("Please enter some text before analyzing.")