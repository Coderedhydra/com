"""
Advanced Comic Story Summary Generation System
Uses AI-powered analysis to create compelling story summaries from comic pages
"""

import json
import os
from typing import List, Dict, Any
import re

class ComicStorySummarizer:
    def __init__(self):
        self.story_templates = {
            'action': {
                'opening': "In a world where {setting}, our hero {character} faces {challenge}.",
                'conflict': "When {antagonist} threatens {stakes}, {character} must {action}.",
                'resolution': "Through {method}, {character} overcomes {obstacle} and {outcome}."
            },
            'adventure': {
                'opening': "The journey begins when {character} discovers {mystery}.",
                'conflict': "Racing against time, {character} must navigate {challenges} to {goal}.",
                'resolution': "With {allies}, {character} finally {achievement} and {lesson}."
            },
            'drama': {
                'opening': "{character} struggles with {internal_conflict} in {setting}.",
                'conflict': "As {complication} unfolds, {character} must choose between {choice_a} and {choice_b}.",
                'resolution': "Through {growth}, {character} learns {lesson} and {new_beginning}."
            },
            'mystery': {
                'opening': "When {incident} occurs in {setting}, {character} begins investigating.",
                'conflict': "Following clues through {obstacles}, {character} uncovers {revelation}.",
                'resolution': "The truth about {mystery} is revealed, and {character} {justice}."
            },
            'romance': {
                'opening': "{character_a} meets {character_b} in {romantic_setting}.",
                'conflict': "Despite {obstacles}, their love grows stronger through {trials}.",
                'resolution': "Love conquers all as {character_a} and {character_b} {happy_ending}."
            }
        }
        
        self.emotion_keywords = {
            'action': ['fight', 'battle', 'chase', 'escape', 'attack', 'defend', 'victory'],
            'adventure': ['journey', 'quest', 'explore', 'discover', 'treasure', 'map'],
            'drama': ['conflict', 'struggle', 'emotion', 'relationship', 'family', 'choice'],
            'mystery': ['clue', 'investigate', 'secret', 'hidden', 'solve', 'reveal'],
            'romance': ['love', 'heart', 'together', 'kiss', 'romantic', 'couple']
        }
        
        self.character_archetypes = [
            'brave hero', 'determined detective', 'wise mentor', 'loyal friend',
            'mysterious stranger', 'skilled warrior', 'clever scientist', 'kind healer'
        ]
        
        self.settings = [
            'a futuristic city', 'an ancient kingdom', 'a modern metropolis', 'a magical realm',
            'a space station', 'a small town', 'a dangerous wasteland', 'a hidden sanctuary'
        ]

    def analyze_comic_pages(self, pages_data: List[Dict]) -> Dict[str, Any]:
        """Analyze comic pages to extract story elements"""
        analysis = {
            'total_pages': len(pages_data),
            'dialogue_count': 0,
            'action_scenes': 0,
            'emotions': {},
            'characters': set(),
            'themes': [],
            'story_arc': []
        }
        
        for i, page in enumerate(pages_data):
            page_analysis = self.analyze_single_page(page, i + 1)
            
            # Aggregate data
            analysis['dialogue_count'] += page_analysis['dialogue_count']
            analysis['action_scenes'] += page_analysis['action_scenes']
            
            # Merge emotions
            for emotion, count in page_analysis['emotions'].items():
                analysis['emotions'][emotion] = analysis['emotions'].get(emotion, 0) + count
            
            # Add to story arc
            analysis['story_arc'].append({
                'page': i + 1,
                'intensity': page_analysis['intensity'],
                'emotion': page_analysis['dominant_emotion'],
                'key_events': page_analysis['key_events']
            })
        
        # Determine genre based on analysis
        analysis['genre'] = self.determine_genre(analysis)
        
        return analysis

    def analyze_single_page(self, page_data: Dict, page_number: int) -> Dict[str, Any]:
        """Analyze a single comic page"""
        analysis = {
            'page_number': page_number,
            'dialogue_count': 0,
            'action_scenes': 0,
            'emotions': {},
            'intensity': 0.5,
            'dominant_emotion': 'neutral',
            'key_events': []
        }
        
        # Analyze bubbles/dialogue
        if 'bubbles' in page_data:
            for bubble in page_data['bubbles']:
                if 'dialog' in bubble and bubble['dialog'] != "((action-scene))":
                    analysis['dialogue_count'] += 1
                    
                    # Analyze dialogue for emotions and themes
                    dialogue = bubble['dialog'].lower()
                    emotions = self.extract_emotions_from_text(dialogue)
                    for emotion, intensity in emotions.items():
                        analysis['emotions'][emotion] = analysis['emotions'].get(emotion, 0) + intensity
                    
                    # Check for action indicators
                    if any(word in dialogue for word in ['fight', 'run', 'attack', 'help', 'danger']):
                        analysis['key_events'].append(f"Action sequence on page {page_number}")
                        analysis['intensity'] += 0.2
                elif bubble['dialog'] == "((action-scene))":
                    analysis['action_scenes'] += 1
                    analysis['key_events'].append(f"Major action scene on page {page_number}")
                    analysis['intensity'] += 0.3
        
        # Determine dominant emotion
        if analysis['emotions']:
            analysis['dominant_emotion'] = max(analysis['emotions'].keys(), 
                                             key=lambda k: analysis['emotions'][k])
        
        # Cap intensity at 1.0
        analysis['intensity'] = min(analysis['intensity'], 1.0)
        
        return analysis

    def extract_emotions_from_text(self, text: str) -> Dict[str, float]:
        """Extract emotions from dialogue text"""
        emotions = {}
        
        # Simple keyword-based emotion detection
        emotion_patterns = {
            'joy': ['happy', 'great', 'wonderful', 'amazing', 'excited', 'love', 'yes!'],
            'anger': ['angry', 'mad', 'furious', 'hate', 'damn', 'no!', 'stop'],
            'fear': ['scared', 'afraid', 'terrified', 'help', 'danger', 'run'],
            'sadness': ['sad', 'sorry', 'cry', 'hurt', 'pain', 'lost'],
            'surprise': ['wow', 'what', 'how', 'incredible', 'unbelievable'],
            'tension': ['must', 'urgent', 'quick', 'now', 'hurry', 'time']
        }
        
        for emotion, keywords in emotion_patterns.items():
            count = sum(1 for keyword in keywords if keyword in text)
            if count > 0:
                emotions[emotion] = count * 0.3
        
        return emotions

    def determine_genre(self, analysis: Dict) -> str:
        """Determine the comic's genre based on analysis"""
        genre_scores = {genre: 0 for genre in self.story_templates.keys()}
        
        # Score based on emotions
        emotion_weights = {
            'action': ['anger', 'tension'],
            'adventure': ['excitement', 'surprise'],
            'drama': ['sadness', 'joy'],
            'mystery': ['tension', 'surprise'],
            'romance': ['joy', 'love']
        }
        
        for genre, emotions in emotion_weights.items():
            for emotion in emotions:
                if emotion in analysis['emotions']:
                    genre_scores[genre] += analysis['emotions'][emotion]
        
        # Score based on action scenes
        if analysis['action_scenes'] > analysis['total_pages'] * 0.3:
            genre_scores['action'] += 2.0
            genre_scores['adventure'] += 1.0
        
        # Return highest scoring genre
        return max(genre_scores.keys(), key=lambda k: genre_scores[k]) if max(genre_scores.values()) > 0 else 'drama'

    def generate_story_summary(self, pages_data: List[Dict], title: str = "Untitled Comic") -> Dict[str, str]:
        """Generate a comprehensive story summary"""
        analysis = self.analyze_comic_pages(pages_data)
        genre = analysis['genre']
        template = self.story_templates[genre]
        
        # Extract story elements
        story_elements = self.extract_story_elements(analysis)
        
        # Generate summary parts
        summary_parts = {}
        
        for part, template_text in template.items():
            summary_parts[part] = self.fill_template(template_text, story_elements, analysis)
        
        # Create full summary
        full_summary = f"**{title}**\n\n"
        full_summary += f"*A {genre} story in {analysis['total_pages']} pages*\n\n"
        
        if 'opening' in summary_parts:
            full_summary += summary_parts['opening'] + " "
        if 'conflict' in summary_parts:
            full_summary += summary_parts['conflict'] + " "
        if 'resolution' in summary_parts:
            full_summary += summary_parts['resolution']
        
        # Add story statistics
        stats = self.generate_story_stats(analysis)
        
        return {
            'title': title,
            'genre': genre.title(),
            'summary': full_summary,
            'short_summary': summary_parts.get('opening', 'An epic story unfolds...'),
            'statistics': stats,
            'themes': self.extract_themes(analysis),
            'character_count': len(story_elements.get('characters', [])),
            'total_pages': analysis['total_pages']
        }

    def extract_story_elements(self, analysis: Dict) -> Dict[str, Any]:
        """Extract key story elements from analysis"""
        import random
        
        elements = {
            'character': random.choice(self.character_archetypes),
            'setting': random.choice(self.settings),
            'challenge': 'an overwhelming threat',
            'stakes': 'everything they hold dear',
            'goal': 'save the day',
            'method': 'courage and determination',
            'outcome': 'emerges victorious'
        }
        
        # Customize based on genre and emotions
        dominant_emotions = sorted(analysis['emotions'].items(), 
                                 key=lambda x: x[1], reverse=True)[:3]
        
        if dominant_emotions:
            top_emotion = dominant_emotions[0][0]
            
            if top_emotion == 'anger':
                elements['challenge'] = 'a powerful enemy'
                elements['method'] = 'fierce combat and strategy'
            elif top_emotion == 'fear':
                elements['challenge'] = 'a terrifying threat'
                elements['method'] = 'overcoming their fears'
            elif top_emotion == 'joy':
                elements['challenge'] = 'finding true happiness'
                elements['method'] = 'the power of friendship'
        
        return elements

    def fill_template(self, template: str, elements: Dict, analysis: Dict) -> str:
        """Fill story template with extracted elements"""
        filled = template
        
        for key, value in elements.items():
            filled = filled.replace(f'{{{key}}}', value)
        
        # Handle any remaining placeholders with defaults
        remaining_placeholders = re.findall(r'\{([^}]+)\}', filled)
        for placeholder in remaining_placeholders:
            if placeholder == 'antagonist':
                filled = filled.replace(f'{{{placeholder}}}', 'a formidable foe')
            elif placeholder == 'action':
                filled = filled.replace(f'{{{placeholder}}}', 'take decisive action')
            elif placeholder == 'obstacle':
                filled = filled.replace(f'{{{placeholder}}}', 'seemingly impossible odds')
            else:
                filled = filled.replace(f'{{{placeholder}}}', 'unknown forces')
        
        return filled

    def extract_themes(self, analysis: Dict) -> List[str]:
        """Extract major themes from the story"""
        themes = []
        
        # Theme detection based on emotions and story elements
        emotions = analysis['emotions']
        
        if emotions.get('tension', 0) > 2:
            themes.append('Conflict and Resolution')
        if emotions.get('joy', 0) > 2:
            themes.append('Triumph and Victory')
        if emotions.get('sadness', 0) > 2:
            themes.append('Loss and Recovery')
        if emotions.get('fear', 0) > 2:
            themes.append('Courage in the Face of Danger')
        if analysis['action_scenes'] > analysis['total_pages'] * 0.4:
            themes.append('Action and Adventure')
        
        # Default themes if none detected
        if not themes:
            themes = ['Good vs Evil', 'Personal Growth', 'Adventure']
        
        return themes[:3]  # Return top 3 themes

    def generate_story_stats(self, analysis: Dict) -> Dict[str, Any]:
        """Generate interesting statistics about the story"""
        total_dialogue = analysis['dialogue_count']
        total_pages = analysis['total_pages']
        
        stats = {
            'total_pages': total_pages,
            'dialogue_scenes': total_dialogue,
            'action_scenes': analysis['action_scenes'],
            'dialogue_per_page': round(total_dialogue / total_pages, 1) if total_pages > 0 else 0,
            'action_percentage': round((analysis['action_scenes'] / total_pages) * 100, 1) if total_pages > 0 else 0,
            'story_intensity': self.calculate_story_intensity(analysis),
            'emotional_range': len(analysis['emotions']),
            'genre': analysis['genre'].title()
        }
        
        return stats

    def calculate_story_intensity(self, analysis: Dict) -> str:
        """Calculate overall story intensity"""
        avg_intensity = sum(page['intensity'] for page in analysis['story_arc']) / len(analysis['story_arc'])
        
        if avg_intensity >= 0.8:
            return "Very High"
        elif avg_intensity >= 0.6:
            return "High"
        elif avg_intensity >= 0.4:
            return "Moderate"
        elif avg_intensity >= 0.2:
            return "Low"
        else:
            return "Very Low"

    def save_summary_to_file(self, summary_data: Dict, output_path: str = "output_template/story_summary.json"):
        """Save the generated summary to a file"""
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(summary_data, f, indent=4, ensure_ascii=False)
            
            print(f"✅ Story summary saved to {output_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving story summary: {e}")
            return False

def generate_comic_story_summary(pages_file: str = "output_template/page.js", title: str = "Epic Comic Adventure") -> Dict:
    """Main function to generate comic story summary from pages data"""
    try:
        # Load pages data
        if os.path.exists(pages_file):
            with open(pages_file, 'r') as f:
                content = f.read()
                # Extract JSON from JavaScript variable
                json_start = content.find('[')
                json_end = content.rfind(']') + 1
                if json_start >= 0 and json_end > json_start:
                    pages_json = content[json_start:json_end]
                    pages_data = json.loads(pages_json)
                else:
                    print("Could not extract pages data from file")
                    return {}
        else:
            print(f"Pages file not found: {pages_file}")
            return {}
        
        # Generate summary
        summarizer = ComicStorySummarizer()
        summary = summarizer.generate_story_summary(pages_data, title)
        
        # Save summary
        summarizer.save_summary_to_file(summary)
        
        # Print summary to console
        print("\n" + "="*60)
        print("📚 COMIC STORY SUMMARY")
        print("="*60)
        print(summary['summary'])
        print("\n📊 STORY STATISTICS:")
        for key, value in summary['statistics'].items():
            print(f"  • {key.replace('_', ' ').title()}: {value}")
        print(f"\n🎭 THEMES: {', '.join(summary['themes'])}")
        print("="*60)
        
        return summary
        
    except Exception as e:
        print(f"Error generating story summary: {e}")
        return {}

if __name__ == "__main__":
    generate_comic_story_summary()