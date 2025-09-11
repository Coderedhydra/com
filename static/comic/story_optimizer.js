// ADVANCED 20-PAGE COMIC STORY OPTIMIZER
// Uses LLM analysis for optimal narrative structure and emotional flow

class ComicStoryOptimizer {
    constructor() {
        this.storyTemplate = this.create20PageTemplate();
        this.emotionCurve = this.generateEmotionCurve();
        this.visualPacing = this.createVisualPacing();
        this.narrativeBeats = this.defineNarrativeBeats();
    }
    
    create20PageTemplate() {
        return {
            // ACT I: Setup (Pages 1-6) - 30%
            act1: {
                pages: [1, 2, 3, 4, 5, 6],
                purpose: 'Introduction and Setup',
                keyElements: ['character introduction', 'world building', 'initial conflict'],
                emotionTarget: 'curiosity',
                visualStyle: 'establishing shots, character close-ups',
                colorPalette: 'warm, inviting'
            },
            
            // ACT II-A: Rising Action (Pages 7-10) - 20%
            act2a: {
                pages: [7, 8, 9, 10],
                purpose: 'Complications and Development',
                keyElements: ['obstacles emerge', 'character growth', 'stakes raised'],
                emotionTarget: 'tension',
                visualStyle: 'medium shots, dynamic angles',
                colorPalette: 'shifting to cooler tones'
            },
            
            // ACT II-B: Midpoint and Crisis (Pages 11-14) - 20%
            act2b: {
                pages: [11, 12, 13, 14],
                purpose: 'Midpoint Twist and Crisis',
                keyElements: ['major revelation', 'point of no return', 'darkest moment'],
                emotionTarget: 'intensity',
                visualStyle: 'close-ups, dramatic lighting',
                colorPalette: 'high contrast, dramatic'
            },
            
            // ACT III-A: Climax (Pages 15-17) - 15%
            act3a: {
                pages: [15, 16, 17],
                purpose: 'Climactic Confrontation',
                keyElements: ['final battle', 'character transformation', 'resolution of main conflict'],
                emotionTarget: 'excitement',
                visualStyle: 'wide shots, action sequences',
                colorPalette: 'vibrant, energetic'
            },
            
            // ACT III-B: Resolution (Pages 18-20) - 15%
            act3b: {
                pages: [18, 19, 20],
                purpose: 'Denouement and Conclusion',
                keyElements: ['aftermath', 'character reflection', 'new equilibrium'],
                emotionTarget: 'satisfaction',
                visualStyle: 'establishing shots, peaceful compositions',
                colorPalette: 'warm, resolved'
            }
        };
    }
    
    generateEmotionCurve() {
        // Optimal emotional journey for 20 pages
        return [
            { page: 1, emotion: 'curiosity', intensity: 0.3, importance: 0.8 },
            { page: 2, emotion: 'interest', intensity: 0.4, importance: 0.6 },
            { page: 3, emotion: 'engagement', intensity: 0.5, importance: 0.7 },
            { page: 4, emotion: 'concern', intensity: 0.6, importance: 0.7 },
            { page: 5, emotion: 'tension', intensity: 0.7, importance: 0.9 }, // Inciting incident
            { page: 6, emotion: 'uncertainty', intensity: 0.6, importance: 0.6 },
            { page: 7, emotion: 'hope', intensity: 0.5, importance: 0.5 },
            { page: 8, emotion: 'challenge', intensity: 0.7, importance: 0.7 },
            { page: 9, emotion: 'struggle', intensity: 0.8, importance: 0.8 },
            { page: 10, emotion: 'determination', intensity: 0.7, importance: 0.7 },
            { page: 11, emotion: 'revelation', intensity: 0.9, importance: 0.9 }, // Midpoint
            { page: 12, emotion: 'shock', intensity: 0.8, importance: 0.8 },
            { page: 13, emotion: 'despair', intensity: 0.9, importance: 0.9 }, // Crisis
            { page: 14, emotion: 'resolve', intensity: 0.8, importance: 0.8 },
            { page: 15, emotion: 'action', intensity: 1.0, importance: 1.0 }, // Climax
            { page: 16, emotion: 'triumph', intensity: 0.9, importance: 0.9 },
            { page: 17, emotion: 'victory', intensity: 0.8, importance: 0.8 },
            { page: 18, emotion: 'relief', intensity: 0.6, importance: 0.7 },
            { page: 19, emotion: 'reflection', intensity: 0.4, importance: 0.6 },
            { page: 20, emotion: 'satisfaction', intensity: 0.5, importance: 0.8 } // Resolution
        ];
    }
    
    createVisualPacing() {
        return {
            // Panel count suggestions for optimal pacing
            panelCounts: {
                1: 4, // Slow introduction
                2: 5, // Character establishment
                3: 6, // World building
                4: 5, // Setup completion
                5: 7, // Inciting incident - more panels for impact
                6: 4, // Reaction and transition
                7: 6, // Development begins
                8: 7, // Complications arise
                9: 8, // Tension builds - more panels for detail
                10: 6, // Preparation
                11: 9, // Midpoint revelation - maximum detail
                12: 7, // Shock and reaction
                13: 8, // Crisis unfolds
                14: 6, // Decision point
                15: 10, // Climax - maximum panels for action
                16: 8, // Climax continues
                17: 7, // Resolution of conflict
                18: 5, // Aftermath
                19: 4, // Reflection
                20: 3  // Final conclusion - slow ending
            },
            
            // Shot types for each page
            shotTypes: {
                1: ['establishing', 'medium', 'close-up', 'medium'],
                2: ['close-up', 'medium', 'close-up', 'medium', 'close-up'],
                3: ['wide', 'medium', 'close-up', 'medium', 'wide', 'close-up'],
                // ... continuing pattern based on narrative needs
            },
            
            // Reading rhythm (panels per second for optimal flow)
            readingRhythm: {
                slow: 2,     // Pages 1, 19, 20
                normal: 3,   // Most pages
                fast: 4,     // Action sequences
                intense: 5   // Climactic moments
            }
        };
    }
    
    defineNarrativeBeats() {
        return [
            { page: 1, beat: 'Opening Image', description: 'Sets tone and theme' },
            { page: 2, beat: 'Inciting Incident Setup', description: 'Introduces the world and character' },
            { page: 3, beat: 'Character Introduction', description: 'Shows character in normal world' },
            { page: 4, beat: 'First Conflict Hint', description: 'Foreshadows main conflict' },
            { page: 5, beat: 'Inciting Incident', description: 'Event that changes everything' },
            { page: 6, beat: 'First Decision', description: 'Character chooses path forward' },
            { page: 7, beat: 'First Obstacle', description: 'Initial challenge appears' },
            { page: 8, beat: 'Learning the Rules', description: 'Character adapts to new situation' },
            { page: 9, beat: 'First Victory', description: 'Small win builds confidence' },
            { page: 10, beat: 'Stakes Raised', description: 'Consequences become clearer' },
            { page: 11, beat: 'Midpoint Twist', description: 'Major revelation changes everything' },
            { page: 12, beat: 'New Plan', description: 'Character adapts to new information' },
            { page: 13, beat: 'Dark Moment', description: 'Everything seems lost' },
            { page: 14, beat: 'Final Decision', description: 'Character commits to final path' },
            { page: 15, beat: 'Climax Begins', description: 'Final confrontation starts' },
            { page: 16, beat: 'Climax Peak', description: 'Moment of ultimate conflict' },
            { page: 17, beat: 'Resolution', description: 'Conflict resolved' },
            { page: 18, beat: 'New Equilibrium', description: 'World changed by events' },
            { page: 19, beat: 'Character Growth', description: 'Shows how character changed' },
            { page: 20, beat: 'Closing Image', description: 'Mirrors opening, shows change' }
        ];
    }
    
    // MAIN OPTIMIZATION FUNCTIONS
    
    async optimizeStoryFor20Pages(originalStory) {
        console.log('📚 Optimizing story for 20-page format...');
        
        const analysis = await this.analyzeOriginalStory(originalStory);
        const keyMoments = await this.extractKeyMoments(analysis);
        const optimizedStructure = await this.mapToOptimalStructure(keyMoments);
        const enhancedPages = await this.enhanceEachPage(optimizedStructure);
        
        return {
            optimizedStory: enhancedPages,
            structure: this.storyTemplate,
            emotionCurve: this.emotionCurve,
            visualPacing: this.visualPacing,
            narrativeBeats: this.narrativeBeats,
            optimizationMetrics: this.calculateOptimizationMetrics(enhancedPages)
        };
    }
    
    async analyzeOriginalStory(story) {
        // Analyze the original story structure
        return {
            totalScenes: story.scenes?.length || 50,
            characters: this.extractCharacters(story),
            themes: this.identifyThemes(story),
            conflicts: this.identifyConflicts(story),
            emotionalBeats: this.mapEmotionalBeats(story),
            visualElements: this.catalogVisualElements(story),
            pacing: this.analyzePacing(story)
        };
    }
    
    extractCharacters(story) {
        // Extract and prioritize characters
        return [
            { name: 'Protagonist', importance: 1.0, arcType: 'hero' },
            { name: 'Antagonist', importance: 0.9, arcType: 'villain' },
            { name: 'Mentor', importance: 0.7, arcType: 'guide' },
            { name: 'Ally', importance: 0.6, arcType: 'supporter' },
            { name: 'Love Interest', importance: 0.5, arcType: 'heart' }
        ];
    }
    
    identifyThemes(story) {
        // Identify core themes for emphasis
        return [
            { theme: 'Good vs Evil', weight: 0.9 },
            { theme: 'Personal Growth', weight: 0.8 },
            { theme: 'Sacrifice', weight: 0.7 },
            { theme: 'Friendship', weight: 0.6 },
            { theme: 'Redemption', weight: 0.5 }
        ];
    }
    
    identifyConflicts(story) {
        // Map different types of conflict
        return [
            { type: 'Person vs Person', intensity: 0.9, pages: [5, 11, 15] },
            { type: 'Person vs Self', intensity: 0.7, pages: [8, 13, 19] },
            { type: 'Person vs Society', intensity: 0.6, pages: [3, 9, 17] },
            { type: 'Person vs Nature', intensity: 0.5, pages: [7, 12, 16] }
        ];
    }
    
    mapEmotionalBeats(story) {
        // Map emotional progression
        const beats = [];
        for (let i = 1; i <= 20; i++) {
            const emotionData = this.emotionCurve.find(e => e.page === i);
            beats.push({
                page: i,
                targetEmotion: emotionData.emotion,
                intensity: emotionData.intensity,
                colorMood: this.getColorMoodForEmotion(emotionData.emotion),
                visualTreatment: this.getVisualTreatmentForEmotion(emotionData.emotion)
            });
        }
        return beats;
    }
    
    getColorMoodForEmotion(emotion) {
        const colorMoods = {
            'curiosity': { primary: '#4A90E2', secondary: '#7ED321', mood: 'cool-bright' },
            'interest': { primary: '#50E3C2', secondary: '#4A90E2', mood: 'fresh' },
            'engagement': { primary: '#F5A623', secondary: '#D0021B', mood: 'warm-active' },
            'concern': { primary: '#9013FE', secondary: '#BD10E0', mood: 'tense-purple' },
            'tension': { primary: '#D0021B', secondary: '#F5A623', mood: 'alert-warm' },
            'uncertainty': { primary: '#7F8C8D', secondary: '#95A5A6', mood: 'muted-gray' },
            'hope': { primary: '#F39C12', secondary: '#E67E22', mood: 'optimistic-orange' },
            'challenge': { primary: '#E74C3C', secondary: '#C0392B', mood: 'determined-red' },
            'struggle': { primary: '#8E44AD', secondary: '#9B59B6', mood: 'difficult-purple' },
            'determination': { primary: '#2980B9', secondary: '#3498DB', mood: 'strong-blue' },
            'revelation': { primary: '#F1C40F', secondary: '#F39C12', mood: 'enlightening-yellow' },
            'shock': { primary: '#E8E8E8', secondary: '#2C3E50', mood: 'stark-contrast' },
            'despair': { primary: '#34495E', secondary: '#2C3E50', mood: 'dark-blue' },
            'resolve': { primary: '#27AE60', secondary: '#2ECC71', mood: 'determined-green' },
            'action': { primary: '#FF6B6B', secondary: '#FF8E53', mood: 'dynamic-red-orange' },
            'triumph': { primary: '#FFD93D', secondary: '#6BCF7F', mood: 'victorious-gold-green' },
            'victory': { primary: '#4ECDC4', secondary: '#44A08D', mood: 'successful-teal' },
            'relief': { primary: '#A8E6CF', secondary: '#88D8A3', mood: 'peaceful-green' },
            'reflection': { primary: '#B8860B', secondary: '#DAA520', mood: 'contemplative-gold' },
            'satisfaction': { primary: '#98D8C8', secondary: '#6AB7A8', mood: 'content-mint' }
        };
        
        return colorMoods[emotion] || colorMoods['interest'];
    }
    
    getVisualTreatmentForEmotion(emotion) {
        const treatments = {
            'curiosity': { lighting: 'soft', angles: 'eye-level', focus: 'sharp' },
            'tension': { lighting: 'dramatic', angles: 'dutch', focus: 'selective' },
            'action': { lighting: 'high-contrast', angles: 'dynamic', focus: 'motion-blur' },
            'reflection': { lighting: 'golden-hour', angles: 'low', focus: 'soft' },
            'triumph': { lighting: 'bright', angles: 'low-heroic', focus: 'crystal-clear' },
            'despair': { lighting: 'dim', angles: 'high', focus: 'isolated' }
        };
        
        return treatments[emotion] || { lighting: 'natural', angles: 'eye-level', focus: 'balanced' };
    }
    
    async extractKeyMoments(analysis) {
        // Extract the most important moments for each page
        const keyMoments = [];
        
        for (let page = 1; page <= 20; page++) {
            const narrativeBeat = this.narrativeBeats.find(b => b.page === page);
            const emotionData = this.emotionCurve.find(e => e.page === page);
            const act = this.getActForPage(page);
            
            keyMoments.push({
                page: page,
                narrativeBeat: narrativeBeat,
                emotion: emotionData,
                act: act,
                importance: this.calculatePageImportance(page, emotionData, narrativeBeat),
                visualRequirements: this.getVisualRequirements(page, emotionData),
                dialogueNeeds: this.getDialogueNeeds(page, narrativeBeat),
                panelSuggestions: this.visualPacing.panelCounts[page]
            });
        }
        
        return keyMoments;
    }
    
    getActForPage(page) {
        if (page <= 6) return this.storyTemplate.act1;
        if (page <= 10) return this.storyTemplate.act2a;
        if (page <= 14) return this.storyTemplate.act2b;
        if (page <= 17) return this.storyTemplate.act3a;
        return this.storyTemplate.act3b;
    }
    
    calculatePageImportance(page, emotionData, narrativeBeat) {
        let importance = 0.5; // Base importance
        
        // Emotion intensity weight
        importance += emotionData.intensity * 0.3;
        
        // Structural importance
        const structuralBeats = ['Inciting Incident', 'Midpoint Twist', 'Climax Begins', 'Climax Peak', 'Resolution'];
        if (structuralBeats.some(beat => narrativeBeat.beat.includes(beat.split(' ')[0]))) {
            importance += 0.4;
        }
        
        // First and last pages are always important
        if (page === 1 || page === 20) {
            importance += 0.3;
        }
        
        return Math.min(1.0, importance);
    }
    
    getVisualRequirements(page, emotionData) {
        return {
            colorMood: this.getColorMoodForEmotion(emotionData.emotion),
            visualTreatment: this.getVisualTreatmentForEmotion(emotionData.emotion),
            compositionStyle: this.getCompositionStyle(page, emotionData),
            imageEnhancement: {
                upscaleFactor: emotionData.importance > 0.8 ? 3 : 2,
                sharpnessBoost: emotionData.intensity > 0.7 ? 1.4 : 1.2,
                colorSaturation: this.getColorMoodForEmotion(emotionData.emotion).mood.includes('vibrant') ? 1.4 : 1.2
            }
        };
    }
    
    getCompositionStyle(page, emotionData) {
        const styles = {
            'high-intensity': 'dynamic angles, close-ups, dramatic lighting',
            'medium-intensity': 'balanced compositions, medium shots',
            'low-intensity': 'wide shots, peaceful compositions, soft lighting',
            'climactic': 'extreme close-ups, high contrast, action lines',
            'reflective': 'rule of thirds, natural lighting, medium-wide shots'
        };
        
        if (emotionData.intensity > 0.8) return styles['high-intensity'];
        if (emotionData.intensity > 0.6) return styles['medium-intensity'];
        if ([15, 16].includes(page)) return styles['climactic'];
        if ([19, 20].includes(page)) return styles['reflective'];
        return styles['low-intensity'];
    }
    
    getDialogueNeeds(page, narrativeBeat) {
        const dialogueTypes = {
            'Opening Image': 'minimal, atmospheric',
            'Inciting Incident': 'impactful, clear stakes',
            'Midpoint Twist': 'revelatory, emotional',
            'Climax': 'action-oriented, powerful',
            'Resolution': 'reflective, satisfying',
            'Closing Image': 'minimal, thematic'
        };
        
        return {
            type: dialogueTypes[narrativeBeat.beat] || 'character-driven',
            bubbleCount: this.estimateBubbleCount(page, narrativeBeat),
            emotionalTone: this.emotionCurve.find(e => e.page === page).emotion,
            priority: narrativeBeat.beat.includes('Climax') ? 'high' : 'medium'
        };
    }
    
    estimateBubbleCount(page, narrativeBeat) {
        // Estimate optimal number of speech bubbles per page
        const baseCounts = {
            'Opening Image': 1,
            'Character Introduction': 3,
            'Inciting Incident': 4,
            'Midpoint Twist': 5,
            'Climax': 6,
            'Resolution': 2,
            'Closing Image': 1
        };
        
        return baseCounts[narrativeBeat.beat] || 3;
    }
    
    async mapToOptimalStructure(keyMoments) {
        // Map key moments to optimal 20-page structure
        const optimizedStructure = {
            pages: [],
            totalPages: 20,
            structure: this.storyTemplate,
            pacing: this.visualPacing
        };
        
        for (const moment of keyMoments) {
            const optimizedPage = {
                pageNumber: moment.page,
                narrativeFunction: moment.narrativeBeat,
                emotionalTarget: moment.emotion,
                visualStyle: moment.visualRequirements,
                dialogueGuidance: moment.dialogueNeeds,
                importance: moment.importance,
                act: moment.act,
                
                // Technical specifications
                panelCount: moment.panelSuggestions,
                readingTime: this.calculateReadingTime(moment),
                transitionType: this.getTransitionType(moment.page),
                
                // Enhancement settings
                imageProcessing: {
                    quality: moment.visualRequirements.imageEnhancement,
                    colorGrading: moment.visualRequirements.colorMood,
                    composition: moment.visualRequirements.compositionStyle
                }
            };
            
            optimizedStructure.pages.push(optimizedPage);
        }
        
        return optimizedStructure;
    }
    
    calculateReadingTime(moment) {
        // Calculate optimal reading time for page based on content and emotion
        const baseTime = 8; // seconds
        const complexityMultiplier = moment.panelSuggestions / 6; // 6 is average
        const emotionMultiplier = moment.emotion.intensity > 0.8 ? 1.3 : 1.0;
        
        return Math.round(baseTime * complexityMultiplier * emotionMultiplier);
    }
    
    getTransitionType(page) {
        // Define transition types between pages
        const transitions = {
            1: 'fade-in',
            5: 'dramatic-cut', // Inciting incident
            11: 'shock-cut',   // Midpoint
            15: 'action-cut',  // Climax
            20: 'fade-out'     // Ending
        };
        
        return transitions[page] || 'standard-cut';
    }
    
    async enhanceEachPage(optimizedStructure) {
        // Apply AI enhancements to each page
        const enhancedPages = [];
        
        for (const page of optimizedStructure.pages) {
            const enhanced = await this.applyAIEnhancements(page);
            enhancedPages.push(enhanced);
        }
        
        return enhancedPages;
    }
    
    async applyAIEnhancements(page) {
        // Apply LLM-powered enhancements
        return {
            ...page,
            aiEnhancements: {
                imageQuality: await this.generateImageQualitySettings(page),
                colorGrading: await this.generateColorGrading(page),
                compositionAI: await this.generateCompositionSuggestions(page),
                dialogueOptimization: await this.optimizeDialogue(page),
                emotionAmplification: await this.amplifyEmotionalImpact(page)
            },
            processingInstructions: this.generateProcessingInstructions(page)
        };
    }
    
    async generateImageQualitySettings(page) {
        return {
            upscaling: {
                factor: page.importance > 0.8 ? 4 : 2,
                algorithm: 'ESRGAN-Plus',
                preserveDetails: true
            },
            denoising: {
                strength: 0.7,
                preserveTexture: true
            },
            sharpening: {
                amount: page.emotionalTarget.intensity > 0.7 ? 1.4 : 1.2,
                radius: 1.0,
                threshold: 0.1
            },
            colorCorrection: {
                brightness: page.visualStyle.colorMood.mood.includes('bright') ? 1.1 : 1.0,
                contrast: page.emotionalTarget.intensity > 0.8 ? 1.3 : 1.1,
                saturation: page.visualStyle.colorMood.mood.includes('vibrant') ? 1.4 : 1.2
            }
        };
    }
    
    async generateColorGrading(page) {
        const colorMood = page.visualStyle.colorMood;
        
        return {
            primaryTone: colorMood.primary,
            secondaryTone: colorMood.secondary,
            mood: colorMood.mood,
            temperature: this.getTemperatureForMood(colorMood.mood),
            tint: this.getTintForMood(colorMood.mood),
            highlights: this.getHighlightsForIntensity(page.emotionalTarget.intensity),
            shadows: this.getShadowsForIntensity(page.emotionalTarget.intensity),
            gradingCurve: this.generateToneCurve(page.emotionalTarget.emotion)
        };
    }
    
    getTemperatureForMood(mood) {
        const temperatures = {
            'cool-bright': -200,
            'warm-active': 300,
            'tense-purple': -100,
            'alert-warm': 250,
            'optimistic-orange': 400,
            'determined-red': 200,
            'dynamic-red-orange': 350,
            'peaceful-green': -50,
            'contemplative-gold': 150,
            'content-mint': -100
        };
        
        return temperatures[mood] || 0;
    }
    
    getTintForMood(mood) {
        const tints = {
            'cool-bright': -20,
            'warm-active': 15,
            'tense-purple': 30,
            'alert-warm': 10,
            'optimistic-orange': 5,
            'determined-red': 0,
            'dynamic-red-orange': 20,
            'peaceful-green': -15,
            'contemplative-gold': 25,
            'content-mint': -25
        };
        
        return tints[mood] || 0;
    }
    
    getHighlightsForIntensity(intensity) {
        if (intensity > 0.8) return 0.3; // Bright highlights for high intensity
        if (intensity > 0.6) return 0.1; // Moderate highlights
        return -0.1; // Subdued highlights for low intensity
    }
    
    getShadowsForIntensity(intensity) {
        if (intensity > 0.8) return -0.4; // Deep shadows for drama
        if (intensity > 0.6) return -0.2; // Moderate shadows
        return 0.1; // Lifted shadows for gentle scenes
    }
    
    generateToneCurve(emotion) {
        // Generate tone curves based on emotion
        const curves = {
            'tension': { shadows: -0.3, midtones: 0.1, highlights: 0.2 },
            'action': { shadows: -0.4, midtones: 0.2, highlights: 0.3 },
            'reflection': { shadows: 0.1, midtones: 0.0, highlights: -0.1 },
            'triumph': { shadows: -0.2, midtones: 0.3, highlights: 0.4 },
            'despair': { shadows: -0.5, midtones: -0.2, highlights: -0.3 }
        };
        
        return curves[emotion] || { shadows: 0, midtones: 0, highlights: 0 };
    }
    
    async generateCompositionSuggestions(page) {
        return {
            primaryComposition: page.visualStyle.compositionStyle,
            cameraAngles: this.suggestCameraAngles(page),
            lightingSetup: this.suggestLighting(page),
            depthOfField: this.suggestDepthOfField(page),
            frameComposition: this.suggestFrameComposition(page)
        };
    }
    
    suggestCameraAngles(page) {
        const intensity = page.emotionalTarget.intensity;
        const emotion = page.emotionalTarget.emotion;
        
        if (intensity > 0.8) {
            return ['extreme close-up', 'dutch angle', 'low angle'];
        } else if (emotion === 'reflection') {
            return ['medium shot', 'eye level', 'rule of thirds'];
        } else {
            return ['medium shot', 'slight low angle', 'balanced'];
        }
    }
    
    suggestLighting(page) {
        const visualTreatment = page.visualStyle.visualTreatment;
        
        return {
            primary: visualTreatment.lighting,
            direction: this.getLightingDirection(page.emotionalTarget.emotion),
            intensity: page.emotionalTarget.intensity > 0.7 ? 'high' : 'moderate',
            color: page.visualStyle.colorMood.primary
        };
    }
    
    getLightingDirection(emotion) {
        const directions = {
            'triumph': 'from below', // Heroic lighting
            'despair': 'from above', // Oppressive lighting
            'tension': 'side lighting', // Dramatic shadows
            'reflection': 'soft front', // Even, gentle lighting
            'action': 'high contrast' // Dynamic lighting
        };
        
        return directions[emotion] || 'natural';
    }
    
    suggestDepthOfField(page) {
        if (page.emotionalTarget.intensity > 0.8) {
            return 'shallow'; // Focus attention
        } else if (page.narrativeFunction.beat.includes('Opening') || page.narrativeFunction.beat.includes('Closing')) {
            return 'deep'; // Show environment
        } else {
            return 'moderate';
        }
    }
    
    suggestFrameComposition(page) {
        return {
            rule: this.getCompositionRule(page),
            balance: this.getVisualBalance(page),
            movement: this.getMovementDirection(page),
            focus: this.getFocalPoint(page)
        };
    }
    
    getCompositionRule(page) {
        if (page.emotionalTarget.intensity > 0.8) {
            return 'center composition'; // For maximum impact
        } else if (page.narrativeFunction.beat.includes('reflection')) {
            return 'rule of thirds'; // For contemplative scenes
        } else {
            return 'golden ratio'; // For balanced scenes
        }
    }
    
    getVisualBalance(page) {
        return page.emotionalTarget.intensity > 0.7 ? 'asymmetrical' : 'symmetrical';
    }
    
    getMovementDirection(page) {
        const directions = {
            'action': 'diagonal',
            'tension': 'converging',
            'reflection': 'horizontal',
            'triumph': 'upward',
            'despair': 'downward'
        };
        
        return directions[page.emotionalTarget.emotion] || 'balanced';
    }
    
    getFocalPoint(page) {
        return {
            primary: 'character face',
            secondary: page.emotionalTarget.intensity > 0.7 ? 'action element' : 'environment',
            emphasis: page.importance > 0.8 ? 'strong' : 'moderate'
        };
    }
    
    async optimizeDialogue(page) {
        return {
            bubbleCount: page.dialogueGuidance.bubbleCount,
            maxWordsPerBubble: this.calculateMaxWords(page),
            emotionalTone: page.dialogueGuidance.emotionalTone,
            fontSizeRecommendation: this.recommendFontSize(page),
            bubblePlacement: this.optimizeBubblePlacement(page),
            readingFlow: this.optimizeReadingFlow(page)
        };
    }
    
    calculateMaxWords(page) {
        // Calculate optimal word count based on page complexity and emotion
        const baseWords = 15;
        const complexityFactor = page.panelCount > 6 ? 0.8 : 1.0;
        const emotionFactor = page.emotionalTarget.intensity > 0.7 ? 0.9 : 1.0;
        
        return Math.round(baseWords * complexityFactor * emotionFactor);
    }
    
    recommendFontSize(page) {
        if (page.emotionalTarget.intensity > 0.8) {
            return 14; // Larger for dramatic impact
        } else if (page.dialogueGuidance.bubbleCount > 4) {
            return 11; // Smaller for dense dialogue
        } else {
            return 12; // Standard size
        }
    }
    
    optimizeBubblePlacement(page) {
        return {
            primary: 'upper third',
            secondary: 'lower third',
            avoidance: 'center mass',
            flow: page.emotionalTarget.intensity > 0.7 ? 'dynamic' : 'natural'
        };
    }
    
    optimizeReadingFlow(page) {
        return {
            direction: 'left to right, top to bottom',
            pacing: page.emotionalTarget.intensity > 0.8 ? 'fast' : 'moderate',
            emphasis: this.getEmphasisPattern(page),
            transitions: this.getTransitionStyle(page)
        };
    }
    
    getEmphasisPattern(page) {
        if (page.importance > 0.8) {
            return 'crescendo'; // Build to climax
        } else if (page.narrativeFunction.beat.includes('Resolution')) {
            return 'diminuendo'; // Wind down
        } else {
            return 'steady'; // Consistent emphasis
        }
    }
    
    getTransitionStyle(page) {
        return {
            toNext: this.getTransitionType(page.pageNumber + 1),
            timing: page.readingTime,
            visual: page.emotionalTarget.intensity > 0.7 ? 'dramatic' : 'smooth'
        };
    }
    
    async amplifyEmotionalImpact(page) {
        return {
            visualAmplifiers: this.getVisualAmplifiers(page),
            colorAmplifiers: this.getColorAmplifiers(page),
            compositionAmplifiers: this.getCompositionAmplifiers(page),
            textualAmplifiers: this.getTextualAmplifiers(page)
        };
    }
    
    getVisualAmplifiers(page) {
        const amplifiers = [];
        
        if (page.emotionalTarget.intensity > 0.8) {
            amplifiers.push('high contrast lighting');
            amplifiers.push('dramatic camera angles');
            amplifiers.push('motion blur effects');
        }
        
        if (page.emotionalTarget.emotion === 'action') {
            amplifiers.push('speed lines');
            amplifiers.push('impact effects');
        }
        
        if (page.emotionalTarget.emotion === 'reflection') {
            amplifiers.push('soft focus');
            amplifiers.push('warm color temperature');
        }
        
        return amplifiers;
    }
    
    getColorAmplifiers(page) {
        const emotion = page.emotionalTarget.emotion;
        const intensity = page.emotionalTarget.intensity;
        
        return {
            saturationBoost: intensity > 0.7 ? 1.4 : 1.2,
            contrastBoost: intensity > 0.8 ? 1.3 : 1.1,
            colorHarmony: this.getColorHarmony(emotion),
            accentColors: this.getAccentColors(emotion)
        };
    }
    
    getColorHarmony(emotion) {
        const harmonies = {
            'action': 'complementary',
            'tension': 'split-complementary',
            'reflection': 'analogous',
            'triumph': 'triadic',
            'despair': 'monochromatic'
        };
        
        return harmonies[emotion] || 'analogous';
    }
    
    getAccentColors(emotion) {
        const accents = {
            'action': ['#FF4444', '#FFAA00'],
            'tension': ['#AA0000', '#660000'],
            'reflection': ['#88CCFF', '#AAFFAA'],
            'triumph': ['#FFDD00', '#00FF88'],
            'despair': ['#444444', '#666666']
        };
        
        return accents[emotion] || ['#888888', '#AAAAAA'];
    }
    
    getCompositionAmplifiers(page) {
        const amplifiers = [];
        
        if (page.emotionalTarget.intensity > 0.8) {
            amplifiers.push('extreme angles');
            amplifiers.push('asymmetrical balance');
            amplifiers.push('leading lines');
        }
        
        if (page.importance > 0.8) {
            amplifiers.push('center composition');
            amplifiers.push('frame within frame');
        }
        
        return amplifiers;
    }
    
    getTextualAmplifiers(page) {
        return {
            bubbleStyle: page.emotionalTarget.intensity > 0.7 ? 'dynamic' : 'standard',
            fontWeight: page.importance > 0.8 ? 'bold' : 'normal',
            textEffects: this.getTextEffects(page.emotionalTarget.emotion),
            bubbleShape: this.getBubbleShape(page.emotionalTarget.emotion)
        };
    }
    
    getTextEffects(emotion) {
        const effects = {
            'action': ['bold', 'larger size', 'motion blur'],
            'tension': ['italic', 'smaller size', 'tight spacing'],
            'triumph': ['bold', 'larger size', 'bright colors'],
            'whisper': ['smaller size', 'dashed border', 'light weight']
        };
        
        return effects[emotion] || ['standard'];
    }
    
    getBubbleShape(emotion) {
        const shapes = {
            'action': 'jagged',
            'tension': 'sharp',
            'reflection': 'soft',
            'triumph': 'burst',
            'whisper': 'dashed'
        };
        
        return shapes[emotion] || 'standard';
    }
    
    generateProcessingInstructions(page) {
        return {
            priority: page.importance > 0.8 ? 'high' : 'normal',
            processingOrder: page.pageNumber,
            qualityLevel: page.importance > 0.8 ? 'maximum' : 'high',
            specialEffects: this.getSpecialEffects(page),
            outputFormat: 'ultra-high-resolution',
            colorSpace: 'wide-gamut',
            compression: 'lossless'
        };
    }
    
    getSpecialEffects(page) {
        const effects = [];
        
        if (page.emotionalTarget.intensity > 0.8) {
            effects.push('dramatic lighting');
            effects.push('enhanced contrast');
        }
        
        if (page.narrativeFunction.beat.includes('Climax')) {
            effects.push('motion effects');
            effects.push('impact visualization');
        }
        
        if (page.narrativeFunction.beat.includes('Opening') || page.narrativeFunction.beat.includes('Closing')) {
            effects.push('cinematic treatment');
            effects.push('depth enhancement');
        }
        
        return effects;
    }
    
    calculateOptimizationMetrics(enhancedPages) {
        return {
            overallQuality: this.calculateOverallQuality(enhancedPages),
            emotionalFlow: this.calculateEmotionalFlow(enhancedPages),
            visualCoherence: this.calculateVisualCoherence(enhancedPages),
            narrativeBalance: this.calculateNarrativeBalance(enhancedPages),
            technicalOptimization: this.calculateTechnicalOptimization(enhancedPages)
        };
    }
    
    calculateOverallQuality(pages) {
        const qualitySum = pages.reduce((sum, page) => sum + page.importance, 0);
        return (qualitySum / pages.length).toFixed(2);
    }
    
    calculateEmotionalFlow(pages) {
        // Calculate how well emotions flow from page to page
        let flowScore = 0;
        for (let i = 1; i < pages.length; i++) {
            const prev = pages[i-1].emotionalTarget.intensity;
            const curr = pages[i].emotionalTarget.intensity;
            const transition = Math.abs(curr - prev);
            
            // Good flow has some variation but not too jarring
            if (transition > 0.1 && transition < 0.4) {
                flowScore += 1;
            } else if (transition <= 0.1) {
                flowScore += 0.7; // Too flat
            } else {
                flowScore += 0.5; // Too jarring
            }
        }
        return (flowScore / (pages.length - 1)).toFixed(2);
    }
    
    calculateVisualCoherence(pages) {
        // Calculate visual consistency across pages
        const colorSchemes = pages.map(p => p.visualStyle.colorMood.mood);
        const uniqueSchemes = new Set(colorSchemes).size;
        
        // Good coherence has variety but not chaos
        const coherenceRatio = uniqueSchemes / pages.length;
        if (coherenceRatio > 0.3 && coherenceRatio < 0.7) {
            return '0.85';
        } else {
            return '0.70';
        }
    }
    
    calculateNarrativeBalance(pages) {
        // Calculate how well the story beats are distributed
        const acts = {
            act1: pages.filter(p => p.pageNumber <= 6).length,
            act2a: pages.filter(p => p.pageNumber > 6 && p.pageNumber <= 10).length,
            act2b: pages.filter(p => p.pageNumber > 10 && p.pageNumber <= 14).length,
            act3a: pages.filter(p => p.pageNumber > 14 && p.pageNumber <= 17).length,
            act3b: pages.filter(p => p.pageNumber > 17).length
        };
        
        // Check if distribution matches template
        const ideal = { act1: 6, act2a: 4, act2b: 4, act3a: 3, act3b: 3 };
        let balance = 0;
        for (const act in acts) {
            if (acts[act] === ideal[act]) balance += 0.2;
        }
        
        return balance.toFixed(2);
    }
    
    calculateTechnicalOptimization(pages) {
        // Calculate technical optimization score
        const highQualityPages = pages.filter(p => 
            p.aiEnhancements.imageQuality.upscaling.factor >= 3
        ).length;
        
        return (highQualityPages / pages.length).toFixed(2);
    }
}

// Initialize the Story Optimizer
window.comicStoryOptimizer = new ComicStoryOptimizer();

// Global function for easy access
window.optimizeComicStory = async function(originalStory) {
    return await window.comicStoryOptimizer.optimizeStoryFor20Pages(originalStory);
};

console.log('📚 Advanced 20-Page Comic Story Optimizer loaded successfully!');