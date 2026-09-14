import re
from textblob import TextBlob
from langdetect import detect

class API:

    def __init__(self):
        self.emotion_lexicon = {
            'Happy': [
                'happy', 'glad', 'joy', 'delighted', 'cheerful', 'pleased', 'smile', 
                'smiling', 'awesome', 'great', 'good', 'wonderful', 'blessed', 
                'fantastic', 'super', 'enjoy', 'enjoying', 'content', 'celebrate'
            ],
            'Sad': [
                'sad', 'unhappy', 'sorrow', 'grief', 'depressed', 'gloomy', 'cry', 
                'crying', 'lonely', 'alone', 'hopeless', 'miserable', 'pain', 'hurt', 
                'heartbroken', 'bad', 'disappointed', 'regret'
            ],
            'Angry': [
                'angry', 'mad', 'furious', 'rage', 'annoyed', 'irritated', 'hate', 
                'hating', 'bitter', 'frustrated', 'offended', 'disgusted', 'wrath'
            ],
            'Fear': [
                'fear', 'afraid', 'scared', 'terrified', 'panic', 'worried', 
                'nervous', 'anxious', 'horror', 'dread', 'frightened', 'danger'
            ],
            'Surprise': [
                'surprise', 'surprised', 'shocked', 'amazed', 'astonished', 
                'unexpected', 'wonder', 'unbelievable', 'stunned'
            ],
            'Excited': [
                'excited', 'thrilled', 'love', 'loved', 'loving', 'passionate', 
                'eager', 'energetic', 'hyped', 'cool', 'adore'
            ]
        }
        
        self.lang_map = {
            'en': 'English', 'hi': 'Hindi', 'es': 'Spanish', 'fr': 'French', 
            'de': 'German', 'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 
            'ja': 'Japanese', 'ko': 'Korean', 'zh-cn': 'Chinese (Simplified)', 
            'zh-tw': 'Chinese (Traditional)', 'ar': 'Arabic', 'bn': 'Bengali', 
            'ur': 'Urdu', 'pa': 'Punjabi', 'gu': 'Gujarati', 'mr': 'Marathi', 
            'ta': 'Tamil', 'te': 'Telugu'
        }

    def sentiment_analysis(self, text):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0.05:
            pos = 0.5 + (polarity * 0.5)
            neg = (1 - pos) * 0.2
            neu = 1 - (pos + neg)
        elif polarity < -0.05:
            neg = 0.5 + (abs(polarity) * 0.5)
            pos = (1 - neg) * 0.2
            neu = 1 - (pos + neg)
        else:
            neu = 0.8
            pos = 0.1
            neg = 0.1
        total = pos + neu + neg
        return {
            'sentiment': {
                'positive': round(pos / total, 2),
                'neutral': round(neu / total, 2),
                'negative': round(neg / total, 2)
            }
        }

    def emotion_analysis(self, text):
        blob = TextBlob(text)
        words = re.findall(r'\b\w+\b', text.lower())
        scores = {k: 0.05 for k in self.emotion_lexicon}

        for word in words:
            for emotion, keywords in self.emotion_lexicon.items():
                if word in keywords:
                    scores[emotion] += 1.0

        pol = blob.sentiment.polarity
        if pol > 0:
            scores['Happy'] += pol * 0.5
            scores['Excited'] += pol * 0.3
        elif pol < 0:
            scores['Sad'] += abs(pol) * 0.4
            scores['Angry'] += abs(pol) * 0.3

        total = sum(scores.values())
        return {
            'emotion': {k: round(v / total, 2) for k, v in scores.items()}
        }

    def language_analysis(self, text):
        try:
            code = detect(text)
            name = self.lang_map.get(code, code.upper())
            return {'language': name, 'code': code}
        except Exception:
            return {'language': 'Unknown', 'code': 'unknown'}