#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import re
import numpy as np
import pandas as pd
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Any
import argparse
import glob
import warnings
import random
from datetime import datetime
warnings.filterwarnings('ignore')

# Базовые импорты
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.decomposition import LatentDirichletAllocation, NMF
from sklearn.metrics import silhouette_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
import time
from datetime import datetime
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import multiprocessing
import concurrent.futures

# Загрузка NLTK данных
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass

# Попытка импорта продвинутых библиотек
try:
    import spacy
    nlp = spacy.load("ru_core_news_sm")
    SPACY_AVAILABLE = True
except:
    SPACY_AVAILABLE = False
    print("spaCy не установлен. Используем базовую обработку.")

try:
    from sentence_transformers import SentenceTransformer
    TRANSFORMER_AVAILABLE = True
except:
    TRANSFORMER_AVAILABLE = False
    print("sentence-transformers не установлен. Используем TF-IDF.")

# Попытка загрузить HuggingFace pipeline для sentiment analysis
try:
    from transformers import pipeline
    HFG_PIPELINE_AVAILABLE = True
except Exception:
    HFG_PIPELINE_AVAILABLE = False
    print("transformers не установлен. Sentiment analysis недоступен.")

# Для multiprocessing: глобальная переменная-анализатор в воркерах
from typing import Any
_WORKER_ANALYZER: Any = None

def _init_worker_analyzer():
    """Инициализация анализатора в процессе-воркере"""
    global _WORKER_ANALYZER
    try:
        _WORKER_ANALYZER = AdvancedBankingAnalyzer()
    except Exception:
        _WORKER_ANALYZER = None

def _worker_analyze(review: Dict[str, Any]) -> Dict[str, Any]:
    """Функция-обёртка для multiprocessing: вызывает анализатор в worker process."""
    global _WORKER_ANALYZER
    if _WORKER_ANALYZER is None:
        try:
            _WORKER_ANALYZER = AdvancedBankingAnalyzer()
        except Exception as e:
            return {'id': review.get('id', 'unknown'), 'error': f'init failed: {e}'}

    try:
        return _WORKER_ANALYZER.analyze_review_themes(review)
    except Exception as e:
        return {'id': review.get('id', 'unknown'), 'error': str(e)}


def load_random_reviews_from_folder(folder_path: str, n: int = None) -> List[Dict[str, Any]]:
    all_reviews = []
    
    # Получаем все JSON файлы в папке
    json_files = glob.glob(os.path.join(folder_path, "*.json"))
    
    if not json_files:
        print(f"В папке {folder_path} не найдено JSON файлов")
        return []
    
    print(f"Найдено {len(json_files)} JSON файлов")
    
    # Загружаем все отзывы из всех файлов
    for json_file in tqdm(json_files, desc="Загрузка файлов"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Обрабатываем разные структуры JSON
                if isinstance(data, list):
                    reviews = data
                elif isinstance(data, dict) and 'reviews' in data:
                    reviews = data['reviews']
                else:
                    reviews = [data]
                
                # Добавляем информацию о файле к каждому отзыву
                for review in reviews:
                    if isinstance(review, dict) and 'text' in review:
                        review['file'] = os.path.basename(json_file)
                        all_reviews.append(review)
        
        except Exception as e:
            print(f"Ошибка при загрузке {json_file}: {e}")
            continue
    
    print(f"Всего загружено {len(all_reviews)} отзывов")
    
    # Если n не указан или n <= 0 — возвращаем все отзывы (в порядке загрузки)
    if n is None or n <= 0:
        print(f"Возвращаем все {len(all_reviews)} отзывов из папки")
        return all_reviews

    # Если запрошено больше, чем есть — используем все
    if n > len(all_reviews):
        print(f"Запрошено {n} отзывов, но доступно только {len(all_reviews)}. Используем все.")
        n = len(all_reviews)

    random_reviews = random.sample(all_reviews, n)
    print(f"Выбрано {len(random_reviews)} случайных отзывов")

    return random_reviews


class AdvancedBankingAnalyzer:
    def __init__(self):
        """Инициализация улучшенного анализатора"""
        
        # Расширенная таксономия банковских тем с детальными паттернами
        self.banking_taxonomy = {
            'Кредитные карты': {
                'keywords': ['кредитная карта', 'кредитка', 'лимит', 'овердрафт', 
                            'грейс период', 'льготный период', 'задолженность'],
                'patterns': [
                    r'\bкредитн\w*\s+карт\w*', r'\bкредитк\w*', r'\bлимит\s+кредит\w*',
                    r'\bовердрафт\w*', r'\bгрейс\s*период\w*', r'\bльготн\w*\s+период\w*',
                    r'\bзадолженност\w*\s+по\s+кредит\w*'
                ],
                'context_words': ['процент', 'ставка', 'платеж', 'долг', 'выплата'],
                'subtopics': ['Лимиты', 'Проценты', 'Льготный период', 'Погашение']
            },
            
            'Дебетовые карты': {
                'keywords': ['дебетовая карта', 'зарплатная', 'пенсионная', 'студенческая'],
                'patterns': [
                    r'\bдебетов\w*\s+карт\w*', r'\bзарплатн\w*\s+карт\w*',
                    r'\bпенсионн\w*\s+карт\w*', r'\bстуденческ\w*\s+карт\w*'
                ],
                'context_words': ['счет', 'баланс', 'пополнение', 'снятие'],
                'subtopics': ['Обслуживание', 'Начисления', 'Типы карт']
            },
            
            'Кешбэк и бонусы': {
                'keywords': ['кешбэк', 'кэшбэк', 'бонус', 'баллы', 'программа лояльности',
                            'возврат', 'начисление', 'привилегии'],
                'patterns': [
                    r'\bк[еэ]шб[еэ]к\w*', r'\bбонус\w*', r'\bбалл\w*', 
                    r'\bпрограмм\w*\s+лояльност\w*', r'\bвозврат\s+средств\w*',
                    r'\bначислен\w*\s+бонус\w*', r'\bпривилеги\w*'
                ],
                'context_words': ['процент', 'категория', 'партнер', 'накопление'],
                'subtopics': ['Начисления', 'Условия', 'Партнеры', 'Использование']
            },
            
            'Комиссии и тарифы': {
                'keywords': ['комиссия', 'тариф', 'плата', 'стоимость', 'абонентская',
                            'обслуживание', 'списание'],
                'patterns': [
                    r'\bкомиссии\w*', r'\bтариф\w*', r'\bплат\w*\s+за\s+\w+',
                    r'\bстоимост\w*\s+обслужива\w*', r'\bабонентск\w*\s+плат\w*',
                    r'\bсписан\w*\s+комисси\w*'
                ],
                'context_words': ['рубль', 'процент', 'месяц', 'год', 'снятие'],
                'subtopics': ['За обслуживание', 'За операции', 'Скрытые комиссии']
            },
            
            'Мобильное приложение': {
                'keywords': ['приложение', 'мобильный банк', 'интерфейс', 'обновление',
                            'ошибка', 'зависает', 'вылетает', 'push'],
                'patterns': [
                    r'\bприложени\w*', r'\bмобильн\w*\s+банк\w*', r'\bинтерфейс\w*',
                    r'\bобновлен\w*\s+приложен\w*', r'\bошибк\w*\s+в\s+приложен\w*',
                    r'\bзависа\w*', r'\bвылета\w*', r'\bпуш[-\s]уведомлен\w*'
                ],
                'context_words': ['телефон', 'смартфон', 'android', 'ios', 'версия'],
                'subtopics': ['Функциональность', 'Ошибки', 'Интерфейс', 'Обновления']
            },
            
            'Техподдержка': {
                'keywords': ['поддержка', 'оператор', 'консультант', 'горячая линия',
                            'чат', 'ожидание', 'компетентность'],
                'patterns': [
                    r'\bподдержк\w*', r'\bоператор\w*', r'\bконсультант\w*',
                    r'\bгорячая\s+лини\w*', r'\bчат\s+с\s+\w*', r'\bожидани\w*\s+ответ\w*',
                    r'\bкомпетентност\w*', r'\bбот\w*'
                ],
                'context_words': ['звонок', 'обращение', 'решение', 'помощь', 'ответ'],
                'subtopics': ['Скорость ответа', 'Качество помощи', 'Каналы связи']
            },
            
            'Переводы и платежи': {
                'keywords': ['перевод', 'платеж', 'оплата', 'транзакция', 'СБП'],
                'patterns': [
                    r'\bперевод\w*', r'\bплатеж\w*', r'\bоплат\w*', r'\bтранзакци\w*',
                    r'\bСБП\b', r'\bсистем\w*\s+быстр\w*\s+платеж\w*'
                ],
                'context_words': ['счет', 'карта', 'деньги', 'средства', 'получатель'],
                'subtopics': ['Внутренние', 'Внешние', 'Международные', 'СБП']
            },
            
            'Банкоматы': {
                'keywords': ['банкомат', 'терминал', 'наличные', 'снятие', 'пополнение'],
                'patterns': [
                    r'\bбанкомат\w*', r'\bтерминал\w*', r'\bналичн\w*',
                    r'\bснят\w*\s+денег\w*', r'\bпополнен\w*\s+карт\w*'
                ],
                'context_words': ['деньги', 'купюра', 'чек', 'экран', 'карта'],
                'subtopics': ['Доступность', 'Работоспособность', 'Лимиты']
            },
            
            'Обслуживание в офисах': {
                'keywords': ['офис', 'отделение', 'очередь', 'сотрудник', 'менеджер'],
                'patterns': [
                    r'\bофис\w*', r'\bотделени\w*', r'\bочеред\w*',
                    r'\bсотрудник\w*\s+банк\w*', r'\bменеджер\w*'
                ],
                'context_words': ['визит', 'прием', 'обслуживание', 'ожидание'],
                'subtopics': ['Очереди', 'Компетентность', 'Вежливость']
            },
            
            'Кредиты и займы': {
                'keywords': ['кредит', 'заем', 'ссуда', 'ипотека', 'автокредит'],
                'patterns': [
                    r'\bкредит\w*', r'\bзайм\w*', r'\bссуд\w*', 
                    r'\bипотек\w*', r'\bавтокредит\w*'
                ],
                # исключаем совпадения, которые на самом деле про кредитные карты
                'exclude_patterns': [
                    r'\bкредитн\w*\s+карт\w*', r'\bкредитк\w*', r'\bкредитная\s+карта\b', r'\bкредитка\b', r'\bкарта\b'
                ],
                'context_words': ['процент', 'ставка', 'платеж', 'одобрение'],
                'subtopics': ['Условия', 'Ставки', 'Одобрение', 'Погашение']
            }
        }
        
        # Инициализация моделей
        self._initialize_models()
        
        # Хранилище результатов
        self.reviews_data = []
        self.theme_clusters = {}
        self.theme_summaries = {}
        
    def _initialize_models(self):
        """Инициализация ML моделей"""
        # Векторизатор с оптимизированными параметрами
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=3000,
            min_df=2,
            max_df=0.85,
            ngram_range=(1, 3),
            token_pattern=r'\b[а-яё]{2,}\b',
            lowercase=True
        )
        
        # Модель для эмбеддингов (если доступна)
        if TRANSFORMER_AVAILABLE:
            try:
                self.sentence_model = SentenceTransformer('cointegrated/rubert-tiny2')
                print("✅ Загружена модель эмбеддингов rubert-tiny2")
            except:
                self.sentence_model = None
                print("⚠️ Не удалось загрузить модель эмбеддингов")
        else:
            self.sentence_model = None
        # Попытка инициализировать sentiment pipeline с blanchefort/rubert
        self.sentiment_pipeline = None
        if HFG_PIPELINE_AVAILABLE:
            try:
                # модель возвращает метки 'positive', 'negative', 'neutral'
                self.sentiment_pipeline = pipeline(
                    'sentiment-analysis',
                    model='blanchefort/rubert-base-cased-sentiment-rusentiment',
                    device=-1
                )
                print("✅ Загружена модель blanchefort/rubert-base-cased-sentiment-rusentiment")
            except Exception as e:
                self.sentiment_pipeline = None
                print(f"⚠️ Не удалось загрузить blanchefort модель: {e}")
            
    def extract_themes_advanced(self, text: str) -> Dict[str, Any]:
        """Продвинутое извлечение тем с контекстом и суммаризацией"""
        
        # Нормализация текста
        text_lower = text.lower()
        sentences = self._split_into_sentences(text)
        
        # Результаты анализа
        detected_themes = {}
        theme_contexts = defaultdict(list)
        theme_sentences = defaultdict(list)
        
        # Анализируем каждое предложение
        for sent_idx, sentence in enumerate(sentences):
            sent_lower = sentence.lower()
            
            # Проверяем каждую тему
            for theme_name, theme_config in self.banking_taxonomy.items():
                theme_score = 0
                matched_keywords = []
                
                # Проверка паттернов
                for pattern in theme_config['patterns']:
                    if re.search(pattern, sent_lower):
                        theme_score += 2.0
                        matches = re.findall(pattern, sent_lower)
                        matched_keywords.extend(matches)
                
                # Проверка ключевых слов
                for keyword in theme_config['keywords']:
                    if keyword in sent_lower:
                        theme_score += 1.5
                        matched_keywords.append(keyword)
                
                # Проверка контекстных слов
                context_bonus = 0
                for context_word in theme_config['context_words']:
                    if context_word in sent_lower:
                        context_bonus += 0.5

                for ep in theme_config.get('exclude_patterns', []):
                    try:
                        if re.search(ep, sent_lower):
                            theme_score = 0
                            break
                    except Exception:
                        pass

                theme_score += context_bonus
                
                # Если тема обнаружена в предложении
                if theme_score > 1.0:
                    if theme_name not in detected_themes:
                        detected_themes[theme_name] = {
                            'score': 0,
                            'keywords': set(),
                            'subtopics': set()
                        }
                    
                    detected_themes[theme_name]['score'] += theme_score
                    detected_themes[theme_name]['keywords'].update(matched_keywords)
                    
                    # Сохраняем контекст
                    context = self._extract_context(sentences, sent_idx, window=1)
                    theme_contexts[theme_name].append({
                        'sentence': sentence,
                        'context': context,
                        'score': theme_score,
                        'keywords': matched_keywords,
                        'sent_idx': sent_idx
                    })
                    
                    theme_sentences[theme_name].append(sentence)
                    
                    # Определяем подтемы
                    for subtopic in theme_config.get('subtopics', []):
                        if subtopic.lower() in sent_lower:
                            detected_themes[theme_name]['subtopics'].add(subtopic)
        
        # Создаем суммаризации для каждой темы
        theme_summaries = {}
        # Определим приоритет тем (чем раньше в списке — тем выше приоритет)
        PRIORITY_ORDER = [
            'Кредитные карты',
            'Дебетовые карты',
            'Кредиты и займы',
            'Кешбэк и бонусы',
            'Комиссии и тарифы',
            'Мобильное приложение',
            'Техподдержка',
            'Переводы и платежи',
            'Банкоматы',
            'Обслуживание в офисах'
        ]
        # карта sent_idx -> list of (theme, ctx)
        sent_map = defaultdict(list)
        for theme_name, contexts in theme_contexts.items():
            for ctx in contexts:
                si = ctx.get('sent_idx')
                if si is not None:
                    sent_map[si].append((theme_name, ctx))

        for si, lst in sent_map.items():
            if len(lst) <= 1:
                continue
            # выбрать тему с минимальным индексом в PRIORITY_ORDER (если тема не в списке — даём низкий приоритет)
            def pr(theme):
                try:
                    return PRIORITY_ORDER.index(theme)
                except ValueError:
                    return len(PRIORITY_ORDER) + 100

            lst_sorted = sorted(lst, key=lambda x: pr(x[0]))
            winner = lst_sorted[0][0]
            losers = [t for t, _ in lst_sorted[1:]]
            for loser in losers:
                # удалить соответствующие контексты
                new_ctxs = [c for c in theme_contexts[loser] if c.get('sent_idx') != si]
                # найти удалённые контексты чтобы скорректировать score
                removed = [c for c in theme_contexts[loser] if c.get('sent_idx') == si]
                removed_score = sum(c.get('score', 0) for c in removed)
                theme_contexts[loser] = new_ctxs
                # удалить предложения из theme_sentences (те, что соответствуют sent_idx)
                try:
                    for c in removed:
                        sent = c.get('sentence')
                        if sent in theme_sentences[loser]:
                            theme_sentences[loser].remove(sent)
                except Exception:
                    pass
                # скорректировать общий скор
                if loser in detected_themes:
                    detected_themes[loser]['score'] = max(0, detected_themes[loser]['score'] - removed_score)
        for theme_name, contexts in theme_contexts.items():
            # Сортируем по релевантности
            contexts.sort(key=lambda x: x['score'], reverse=True)
            
            # Берем наиболее релевантные предложения
            top_sentences = [ctx['sentence'] for ctx in contexts[:3]]
            
            # Создаем суммаризацию
            summary = self._create_theme_summary(
                theme_name, 
                top_sentences,
                list(detected_themes[theme_name]['keywords']),
                list(detected_themes[theme_name]['subtopics'])
            )
            
            theme_summaries[theme_name] = summary
        
        # Фильтруем темы по порогу
        filtered_themes = {
            theme: data for theme, data in detected_themes.items()
            if data['score'] > 2.0
        }

        # Пост-фильтр: если одновременно найдены 'Кредитные карты' и 'Кредиты и займы',
        try:
            if 'Кредитные карты' in filtered_themes and 'Кредиты и займы' in filtered_themes:
                card_score = detected_themes.get('Кредитные карты', {}).get('score', 0)
                loan_score = detected_themes.get('Кредиты и займы', {}).get('score', 0)
                card_count = len(theme_sentences.get('Кредитные карты', []))
                loan_count = len(theme_sentences.get('Кредиты и займы', []))

                # если карты доминируют — удаляем кредиты
                if card_score >= loan_score or card_count >= loan_count:
                    # remove loan theme
                    filtered_themes.pop('Кредиты и займы', None)
                    if 'Кредиты и займы' in theme_contexts:
                        theme_contexts.pop('Кредиты и займы', None)
                    if 'Кредиты и займы' in theme_summaries:
                        theme_summaries.pop('Кредиты и займы', None)
                    if 'Кредиты и займы' in theme_sentences:
                        theme_sentences.pop('Кредиты и займы', None)
                    if 'Кредиты и займы' in detected_themes:
                        detected_themes.pop('Кредиты и займы', None)
        except Exception:
            pass
        
        return {
            'themes': list(filtered_themes.keys()),
            'theme_details': filtered_themes,
            'theme_contexts': dict(theme_contexts),
            'theme_summaries': theme_summaries,
            'theme_sentences': dict(theme_sentences)
        }
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Разбивка текста на предложения"""
        if SPACY_AVAILABLE:
            doc = nlp(text)
            return [sent.text.strip() for sent in doc.sents]
        else:
            # Базовая разбивка по знакам препинания
            sentences = re.split(r'[.!?]+', text)
            return [s.strip() for s in sentences if s.strip()]
    
    def _extract_context(self, sentences: List[str], idx: int, window: int = 1) -> str:
        """Извлечение контекста вокруг предложения"""
        start_idx = max(0, idx - window)
        end_idx = min(len(sentences), idx + window + 1)
        
        context_sentences = sentences[start_idx:end_idx]
        return ' '.join(context_sentences)
    
    def _create_theme_summary(self, theme: str, sentences: List[str], 
                             keywords: List[str], subtopics: List[str]) -> Dict[str, Any]:
        """Создание суммаризации для темы"""
        # Объединяем предложения
        full_text = ' '.join(sentences[:3])  # Максимум 3 предложения
        
        # Убираем повторы и создаем краткую выжимку
        if len(full_text) > 200:
            # Оставляем только ключевые части
            summary_text = self._compress_text(full_text, keywords)
        else:
            summary_text = full_text
        
        return {
            'theme': theme,
            'summary': summary_text,
            'key_points': keywords[:5],  # Топ-5 ключевых слов
            'subtopics': subtopics,
            'sentence_count': len(sentences)
        }
    
    def _compress_text(self, text: str, keywords: List[str], max_length: int = 200) -> str:
        """Сжатие текста с сохранением ключевой информации"""
        sentences = self._split_into_sentences(text)
        
        # Оцениваем важность каждого предложения
        sentence_scores = []
        for sentence in sentences:
            score = 0
            sent_lower = sentence.lower()
            
            # Считаем вхождения ключевых слов
            for keyword in keywords:
                if keyword in sent_lower:
                    score += 1
            
            sentence_scores.append((sentence, score))
        
        # Сортируем по важности
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Собираем сжатый текст
        compressed = []
        current_length = 0
        
        for sentence, _ in sentence_scores:
            if current_length + len(sentence) <= max_length:
                compressed.append(sentence)
                current_length += len(sentence)
            else:
                break
        
        return ' '.join(compressed)
    
    def analyze_review_themes(self, review: Dict[str, Any]) -> Dict[str, Any]:
        """Полный анализ тем в отзыве"""
        text = review['text']
        rating = review.get('rating', None)
        
        # Извлекаем темы
        theme_analysis = self.extract_themes_advanced(text)
        
        # Анализируем тональность для каждой темы (правилами и blanchefort если доступен)
        theme_sentiments = {}
        theme_sentiments_detailed = {}
        for theme in theme_analysis['themes']:
            theme_sentences = theme_analysis['theme_sentences'].get(theme, [])
            if theme_sentences:
                # Анализируем тональность на основе предложений темы (простой метод)
                sentiment = self._analyze_theme_sentiment(theme_sentences, rating)
                theme_sentiments[theme] = sentiment

                # Дополнительная оценка с помощью blanchefort модели
                blanchefort_score = None
                blanchefort_label = None
                blanchefort_confidence = None
                if hasattr(self, 'sentiment_pipeline') and self.sentiment_pipeline is not None:
                    try:
                        sentiment_res = self._sentiment_analysis_for_text(' '.join(theme_sentences))
                        blanchefort_score = sentiment_res.get('score')
                        blanchefort_label = sentiment_res.get('label')
                        blanchefort_confidence = sentiment_res.get('confidence')
                    except Exception:
                        blanchefort_score = None
                        blanchefort_label = None
                        blanchefort_confidence = None

                theme_sentiments_detailed[theme] = {
                    'rule_based': sentiment,
                    'blanchefort_label': blanchefort_label,
                    'blanchefort_score': blanchefort_score,
                    'blanchefort_confidence': blanchefort_confidence
                }
        
        # Общая тональность
        overall_sentiment = self._analyze_overall_sentiment(text, rating)
        
        return {
            'id': review.get('id', 'unknown'),
            'text': text,
            'rating': rating,
            'date': review.get('date', None),
            'file': review.get('file', 'unknown'),
            'predicted_themes': theme_analysis['themes'],
            'theme_sentiments': theme_sentiments,
            'theme_sentiments_detailed': theme_sentiments_detailed,
            'theme_details': None,  # Заполним позже
            'theme_summaries': theme_analysis['theme_summaries'],
            'theme_contexts': {
                theme: [ctx['context'] for ctx in contexts[:2]]  # Топ-2 контекста
                for theme, contexts in theme_analysis['theme_contexts'].items()
            },
            'overall_sentiment': overall_sentiment,
            'analysis_confidence': None  # Заполним позже
        }
    
    def _analyze_theme_sentiment(self, sentences: List[str], rating: int = None) -> str:
        """Анализ тональности для конкретной темы"""
        # Паттерны для определения тональности
        positive_patterns = [
            'отлично', 'прекрасно', 'удобно', 'быстро', 'хорошо', 'понравилось',
            'рекомендую', 'выгодно', 'качественно', 'профессионально'
        ]
        
        negative_patterns = [
            'плохо', 'ужасно', 'медленно', 'неудобно', 'проблема', 'ошибка',
            'не работает', 'обман', 'разочарован', 'отвратительно',
            # грубые выражения и ругательства — добавить базовые формы
            'гад', 'урод', 'дурак', 'идиот', 'тупой'
        ]
        
        # Подсчет позитивных и негативных сигналов
        positive_score = 0
        negative_score = 0
        
        combined_text = ' '.join(sentences).lower()
        
        for pattern in positive_patterns:
            if pattern in combined_text:
                positive_score += 1
        
        for pattern in negative_patterns:
            if pattern in combined_text:
                negative_score += 1
        
        # Учитываем рейтинг, если есть
        if rating is not None:
            if rating >= 4:
                positive_score += 2
            elif rating <= 2:
                negative_score += 2
        
        # Определяем итоговую тональность
        if positive_score > negative_score:
            return 'positive'
        elif negative_score > positive_score:
            return 'negative'
        else:
            return 'neutral'
    
    def _analyze_overall_sentiment(self, text: str, rating: int = None) -> str:
        """Общий анализ тональности"""
        return self._analyze_theme_sentiment([text], rating)

    def _sentiment_analysis_for_text(self, text: str) -> Dict[str, Any]:
        """Оценивает тональность текста с помощью blanchefort модели."""
        if not hasattr(self, 'sentiment_pipeline') or self.sentiment_pipeline is None:
            raise RuntimeError('sentiment pipeline не инициализирован')

        # Ограничим длину текста чтобы не превысить лимиты
        snippet = text.strip()
        if len(snippet) > 1000:
            snippet = snippet[:1000]

        res = self.sentiment_pipeline(snippet)
        # res обычно: [{'label': 'positive', 'score': 0.85}]
        if not res:
            return {'label': None, 'score': None, 'confidence': None}

        label = res[0].get('label')
        confidence = res[0].get('score')

        # Конвертируем в score (positive=1, neutral=0, negative=-1)
        score_mapping = {
            'positive': 1.0,
            'neutral': 0.0,
            'negative': -1.0
        }
        
        score = score_mapping.get(label, 0.0)

        return {
            'label': label, 
            'score': score,
            'confidence': confidence
        }
    
    def process_reviews_batch(self, reviews: List[Dict[str, Any]], 
                            batch_size: int = 50) -> List[Dict[str, Any]]:
        """Пакетная обработка отзывов"""
        results = []
        
        for i in tqdm(range(0, len(reviews), batch_size), desc="Обработка отзывов"):
            batch = reviews[i:i + batch_size]
            
            for review in batch:
                try:
                    result = self.analyze_review_themes(review)
                    results.append(result)
                except Exception as e:
                    print(f"Ошибка при обработке отзыва {review.get('id', 'unknown')}: {e}")
                    continue
        
        return results

    def process_reviews_parallel(self, reviews: List[Dict[str, Any]], *,
                                 batch_size: int = 50,
                                 workers: int | None = None,
                                 mode: str = 'process') -> List[Dict[str, Any]]:
        """Параллельная обработка отзывов."""
        if not reviews:
            return []

        if workers is None:
            workers = max(1, min(4, multiprocessing.cpu_count()))

        results = []

        if mode == 'process':
            # multiprocessing: каждый воркер инициализирует свой AdvancedBankingAnalyzer
            with multiprocessing.Pool(processes=workers, initializer=_init_worker_analyzer) as pool:
                for res in tqdm(pool.imap(_worker_analyze, reviews), total=len(reviews), desc="Обработка отзывов (parallel)"):
                    results.append(res)
        elif mode == 'thread':
            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
                futures = [ex.submit(self.analyze_review_themes, r) for r in reviews]
                for f in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Обработка отзывов (threads)"):
                    try:
                        results.append(f.result())
                    except Exception as e:
                        results.append({'error': str(e)})

            if results and len(results) != len(reviews):
                # fallback to simple map
                results = [self.analyze_review_themes(r) for r in reviews]
        else:
            raise ValueError("Unknown mode for process_reviews_parallel: choose 'process' or 'thread'")

        return results
    
    def generate_theme_report(self, analyzed_reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Генерация отчета по темам"""
        theme_stats = defaultdict(lambda: {
            'count': 0,
            'sentiments': [],
            'ratings': [],
            'summaries': [],
            'keywords': set(),
            'subtopics': set()
        })
        
        # Собираем статистику
        for review in analyzed_reviews:
            for theme in review['predicted_themes']:
                theme_stats[theme]['count'] += 1
                theme_stats[theme]['sentiments'].append(
                    review['theme_sentiments'].get(theme, 'neutral')
                )
                if review['rating'] is not None:
                    theme_stats[theme]['ratings'].append(review['rating'])
                
                # Собираем суммаризации
                if theme in review['theme_summaries']:
                    summary = review['theme_summaries'][theme]
                    theme_stats[theme]['summaries'].append(summary['summary'])
                    theme_stats[theme]['keywords'].update(summary.get('key_points', []))
                    theme_stats[theme]['subtopics'].update(summary.get('subtopics', []))
        
        # Формируем итоговый отчет
        report = {}
        for theme, stats in theme_stats.items():
            sentiment_counts = Counter(stats['sentiments'])
            
            report[theme] = {
                'total_mentions': stats['count'],
                'average_rating': float(np.mean(stats['ratings'])) if stats['ratings'] else None,
                'sentiment_distribution': dict(sentiment_counts),
                'top_keywords': list(stats['keywords'])[:10],
                'subtopics': list(stats['subtopics']),
                'sample_summaries': stats['summaries'][:3],  # Топ-3 суммаризации
                'sentiment_percentages': {
                    sent: (count / stats['count'] * 100) if stats['count'] > 0 else 0
                    for sent, count in sentiment_counts.items()
                }
            }
        
        return report
    
    def save_analysis_results(self, analyzed_reviews: List[Dict[str, Any]], 
                            theme_report: Dict[str, Any],
                            output_file: str = 'banking_analysis_results.json'):
        """Сохранение результатов анализа"""
        
        # Вычисляем средний рейтинг
        ratings = [r['rating'] for r in analyzed_reviews if r['rating'] is not None]
        avg_rating = float(np.mean(ratings)) if ratings else None
        
        # Подготовка данных для сохранения
        results = {
            'metadata': {
                'total_reviews_analyzed': len(analyzed_reviews),
                'total_themes_identified': len(theme_report),
                'average_rating': avg_rating,
                'test_reviews_count': len(analyzed_reviews),
                'themes_list': sorted(list(theme_report.keys())),
                'analysis_timestamp': datetime.now().isoformat(),
                'model_version': '4.0'
            },
            'theme_statistics': None,  # Заполним позже
            'test_reviews_analysis': analyzed_reviews
        }
        
        # Рекурсивная конвертация не-сериализуемых типов (set -> list)
        def _make_json_serializable(obj):
            if isinstance(obj, dict):
                return {k: _make_json_serializable(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [_make_json_serializable(v) for v in obj]
            if isinstance(obj, set):
                return [_make_json_serializable(v) for v in list(obj)]
            # numpy types
            if isinstance(obj, np.generic):
                return obj.item()
            return obj
        
        serializable_results = _make_json_serializable(results)
        
        # Сохранение в JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, ensure_ascii=False, indent=2)
        
        print(f"Результаты сохранены в {output_file}")
        return output_file


def main():
    """Основная функция для запуска анализа"""
    parser = argparse.ArgumentParser(description='Анализ банковских отзывов')
    parser.add_argument('--folder', type=str, default='out_cleaned',
                       help='Папка с JSON файлами отзывов')
    parser.add_argument('--n', type=int, default=100,
                       help='Количество случайных отзывов для анализа')
    parser.add_argument('--all', action='store_true', help='Загрузить все отзывы из папки (игнорирует --n)')
    parser.add_argument('--output', type=str, default='banking_analysis_results.json',
                       help='Выходной файл с результатами')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Система анализа банковских отзывов v4.0")
    print("=" * 60)
    
    # Загружаем отзывы (все или n случайных)
    if args.all:
        print(f"\nЗагрузка всех отзывов из папки {args.folder}...")
        reviews = load_random_reviews_from_folder(args.folder, None)
    else:
        print(f"\nЗагрузка {args.n} случайных отзывов из папки {args.folder}...")
        reviews = load_random_reviews_from_folder(args.folder, args.n)
    
    if not reviews:
        print("Не удалось загрузить отзывы. Проверьте путь к папке.")
        return
    
    # Инициализируем анализатор
    print("\nИнициализация анализатора...")
    analyzer = AdvancedBankingAnalyzer()
    
    # Обрабатываем отзывы
    print(f"\nАнализ {len(reviews)} отзывов...")
    analyzed_reviews = analyzer.process_reviews_batch(reviews, batch_size=50)
    
    if not analyzed_reviews:
        print("Не удалось проанализировать отзывы.")
        return
    
    # Генерируем отчет по темам
    print("\nГенерация отчета по темам...")
    theme_report = analyzer.generate_theme_report(analyzed_reviews)
    
    # Сохраняем результаты
    print(f"\nСохранение результатов в {args.output}...")
    output_file = analyzer.save_analysis_results(
        analyzed_reviews, 
        theme_report, 
        output_file=args.output
    )
    
    # Краткая статистика
    print("\n" + "=" * 60)
    print("КРАТКАЯ СТАТИСТИКА")
    print("=" * 60)
    print(f"Всего проанализировано отзывов: {len(analyzed_reviews)}")
    print(f"Обнаружено уникальных тем: {len(theme_report)}")
    
    # Топ-5 тем по упоминаниям
    theme_counts = [(theme, data['total_mentions']) 
                    for theme, data in theme_report.items()]
    theme_counts.sort(key=lambda x: x[1], reverse=True)
    
    print("\nТоп-5 тем по упоминаниям:")
    for i, (theme, count) in enumerate(theme_counts[:5], 1):
        print(f"  {i}. {theme}: {count} упоминаний")
    
    # Распределение рейтингов
    ratings = [r['rating'] for r in analyzed_reviews if r['rating'] is not None]
    if ratings:
        avg_rating = np.mean(ratings)
        print(f"\nСредний рейтинг: {avg_rating:.2f}")
        
        rating_dist = Counter(ratings)
        print("Распределение рейтингов:")
        for rating in sorted(rating_dist.keys()):
            count = rating_dist[rating]
            print(f"  {rating} звезд: {count} отзывов ({count/len(ratings)*100:.1f}%)")
    
    print("\n" + "=" * 60)
    print(f"Анализ завершен! Результаты сохранены в: {output_file}")
    print("=" * 60)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nАнализ прерван пользователем")
    except Exception as e:
        print(f"\n\nОшибка при выполнении: {e}")
        import traceback
        traceback.print_exc()