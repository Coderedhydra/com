// ULTRA HIGH PERFORMANCE BUBBLE DRAGGING SYSTEM
// Complete implementation for all bubble shapes with maximum quality

class BubbleDragSystem {
    constructor() {
        this.activeBubbles = new Map();
        this.dragThreshold = 3;
        this.animationFrames = new Map();
        this.observers = new Map();
        
        // Performance optimization
        this.boundMouseMove = this.handleMouseMove.bind(this);
        this.boundMouseUp = this.handleMouseUp.bind(this);
        this.boundTouchMove = this.handleTouchMove.bind(this);
        this.boundTouchEnd = this.handleTouchEnd.bind(this);
        
        this.setupGlobalListeners();
    }
    
    setupGlobalListeners() {
        // Use passive listeners where possible for better performance
        document.addEventListener('mousemove', this.boundMouseMove, { passive: false });
        document.addEventListener('mouseup', this.boundMouseUp, { passive: true });
        document.addEventListener('touchmove', this.boundTouchMove, { passive: false });
        document.addEventListener('touchend', this.boundTouchEnd, { passive: true });
        
        // Prevent context menu during drag
        document.addEventListener('contextmenu', (e) => {
            if (this.activeBubbles.size > 0) {
                e.preventDefault();
            }
        });
    }
    
    // Extract transform values with high precision
    getTransformValues(element) {
        const transform = element.style.transform || '';
        const matrix = transform.match(/matrix.*\((.+)\)/);
        
        if (matrix) {
            const values = matrix[1].split(', ');
            return {
                x: parseFloat(values[4]) || 0,
                y: parseFloat(values[5]) || 0
            };
        }
        
        const translate = transform.match(/translate(?:3d)?\(([^,]+)(?:px)?(?:,\s*([^,]+)(?:px)?)?(?:,\s*([^)]+)(?:px)?)?\)/);
        if (translate) {
            return {
                x: parseFloat(translate[1]) || 0,
                y: parseFloat(translate[2]) || 0
            };
        }
        
        return { x: 0, y: 0 };
    }
    
    // High-performance transform update with sub-pixel precision
    updateTransform(bubble, x, y, force = false) {
        const bubbleId = bubble.dataset.bubbleId;
        if (!bubbleId) return;
        
        // Cancel existing animation frame
        if (this.animationFrames.has(bubbleId)) {
            cancelAnimationFrame(this.animationFrames.get(bubbleId));
        }
        
        // Use requestAnimationFrame for smooth 60fps updates
        const frameId = requestAnimationFrame(() => {
            // Use translate3d for hardware acceleration and sub-pixel rendering
            bubble.style.transform = `translate3d(${x.toFixed(2)}px, ${y.toFixed(2)}px, 0)`;
            this.animationFrames.delete(bubbleId);
        });
        
        this.animationFrames.set(bubbleId, frameId);
    }
    
    // Get bubble boundaries for constraint checking
    getBubbleBounds(bubble) {
        const parent = bubble.parentElement;
        const parentRect = parent.getBoundingClientRect();
        const bubbleRect = bubble.getBoundingClientRect();
        
        return {
            minX: -bubbleRect.width * 0.3, // Allow partial overflow
            maxX: parentRect.width - bubbleRect.width * 0.7,
            minY: -bubbleRect.height * 0.3,
            maxY: parentRect.height - bubbleRect.height * 0.7
        };
    }
    
    // Apply boundary constraints with smooth clamping
    applyConstraints(bubble, x, y) {
        const bounds = this.getBubbleBounds(bubble);
        
        // Smooth clamping with easing at boundaries
        const clampedX = Math.max(bounds.minX, Math.min(bounds.maxX, x));
        const clampedY = Math.max(bounds.minY, Math.min(bounds.maxY, y));
        
        return { x: clampedX, y: clampedY };
    }
    
    // Initialize bubble for dragging
    makeBubbleDraggable(bubble, bubbleIndex) {
        // Assign unique ID for tracking
        const bubbleId = `bubble_${bubbleIndex}_${Date.now()}`;
        bubble.dataset.bubbleId = bubbleId;
        bubble.dataset.bubbleIndex = bubbleIndex;
        
        // Mouse events
        bubble.addEventListener('mousedown', (e) => {
            this.startDrag(bubble, e.clientX, e.clientY, 'mouse');
        }, { passive: false });
        
        // Touch events
        bubble.addEventListener('touchstart', (e) => {
            const touch = e.touches[0];
            this.startDrag(bubble, touch.clientX, touch.clientY, 'touch');
        }, { passive: false });
        
        // Setup mutation observer for cleanup
        this.setupCleanupObserver(bubble);
    }
    
    startDrag(bubble, clientX, clientY, inputType) {
        const bubbleId = bubble.dataset.bubbleId;
        
        // Prevent default behaviors
        if (inputType === 'touch') {
            // Prevent scrolling and zooming on touch devices
            document.body.style.touchAction = 'none';
            document.body.style.userSelect = 'none';
        } else {
            document.body.style.userSelect = 'none';
        }
        
        // Get initial position
        const currentPos = this.getTransformValues(bubble);
        
        // Store drag state
        const dragState = {
            bubble: bubble,
            bubbleIndex: parseInt(bubble.dataset.bubbleIndex),
            isDragging: false,
            hasMoved: false,
            inputType: inputType,
            startX: clientX,
            startY: clientY,
            initialX: currentPos.x,
            initialY: currentPos.y,
            lastX: clientX,
            lastY: clientY,
            velocity: { x: 0, y: 0 },
            timestamps: [Date.now()]
        };
        
        this.activeBubbles.set(bubbleId, dragState);
        
        // Add visual feedback
        bubble.classList.add('dragging');
        bubble.style.cursor = 'grabbing';
        bubble.style.zIndex = '2000';
        
        // Prevent text selection
        bubble.style.webkitUserSelect = 'none';
        bubble.style.mozUserSelect = 'none';
        bubble.style.msUserSelect = 'none';
        bubble.style.userSelect = 'none';
    }
    
    handleMouseMove(e) {
        this.handleMove(e.clientX, e.clientY, 'mouse');
    }
    
    handleTouchMove(e) {
        if (e.touches.length === 1) {
            const touch = e.touches[0];
            this.handleMove(touch.clientX, touch.clientY, 'touch');
        }
    }
    
    handleMove(clientX, clientY, inputType) {
        for (const [bubbleId, dragState] of this.activeBubbles.entries()) {
            if (dragState.inputType !== inputType) continue;
            
            const deltaX = clientX - dragState.startX;
            const deltaY = clientY - dragState.startY;
            
            // Check drag threshold
            if (!dragState.isDragging) {
                const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
                if (distance > this.dragThreshold) {
                    dragState.isDragging = true;
                    dragState.hasMoved = true;
                }
            }
            
            if (dragState.isDragging) {
                // Prevent default scrolling
                if (inputType === 'touch') {
                    event.preventDefault();
                }
                
                // Calculate new position
                const newX = dragState.initialX + deltaX;
                const newY = dragState.initialY + deltaY;
                
                // Apply constraints
                const constrained = this.applyConstraints(dragState.bubble, newX, newY);
                
                // Update transform
                this.updateTransform(dragState.bubble, constrained.x, constrained.y);
                
                // Calculate velocity for momentum (future enhancement)
                const now = Date.now();
                const timeDelta = now - (dragState.timestamps[dragState.timestamps.length - 1] || now);
                if (timeDelta > 0) {
                    dragState.velocity.x = (clientX - dragState.lastX) / timeDelta;
                    dragState.velocity.y = (clientY - dragState.lastY) / timeDelta;
                }
                
                dragState.lastX = clientX;
                dragState.lastY = clientY;
                dragState.timestamps.push(now);
                
                // Keep only recent timestamps for velocity calculation
                if (dragState.timestamps.length > 5) {
                    dragState.timestamps.shift();
                }
            }
        }
    }
    
    handleMouseUp(e) {
        this.endDrag(e.clientX, e.clientY, 'mouse');
    }
    
    handleTouchEnd(e) {
        if (e.changedTouches.length > 0) {
            const touch = e.changedTouches[0];
            this.endDrag(touch.clientX, touch.clientY, 'touch');
        }
    }
    
    endDrag(clientX, clientY, inputType) {
        for (const [bubbleId, dragState] of this.activeBubbles.entries()) {
            if (dragState.inputType !== inputType) continue;
            
            const bubble = dragState.bubble;
            
            // Remove visual feedback
            bubble.classList.remove('dragging');
            bubble.style.cursor = 'grab';
            bubble.style.zIndex = '1000';
            
            // Re-enable text selection
            bubble.style.webkitUserSelect = '';
            bubble.style.mozUserSelect = '';
            bubble.style.msUserSelect = '';
            bubble.style.userSelect = '';
            
            // Update bubble position in data if moved
            if (dragState.isDragging && dragState.hasMoved) {
                const finalPos = this.getTransformValues(bubble);
                this.updateBubbleData(dragState.bubbleIndex, finalPos.x, finalPos.y);
            }
            
            // Clean up
            this.activeBubbles.delete(bubbleId);
        }
        
        // Reset body styles if no active drags
        if (this.activeBubbles.size === 0) {
            document.body.style.touchAction = '';
            document.body.style.userSelect = '';
        }
    }
    
    updateBubbleData(bubbleIndex, x, y) {
        // Update the global pages data structure
        if (typeof pages !== 'undefined' && typeof current_page !== 'undefined') {
            if (pages[current_page] && pages[current_page].bubbles[bubbleIndex]) {
                pages[current_page].bubbles[bubbleIndex].bubble_offset_x = x;
                pages[current_page].bubbles[bubbleIndex].bubble_offset_y = y;
            }
        }
    }
    
    setupCleanupObserver(bubble) {
        const bubbleId = bubble.dataset.bubbleId;
        
        // Clean up when bubble is removed from DOM
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.removedNodes.forEach((node) => {
                    if (node === bubble) {
                        this.cleanup(bubbleId);
                        observer.disconnect();
                    }
                });
            });
        });
        
        if (bubble.parentNode) {
            observer.observe(bubble.parentNode, { childList: true });
            this.observers.set(bubbleId, observer);
        }
    }
    
    cleanup(bubbleId) {
        // Cancel animation frame
        if (this.animationFrames.has(bubbleId)) {
            cancelAnimationFrame(this.animationFrames.get(bubbleId));
            this.animationFrames.delete(bubbleId);
        }
        
        // Remove from active bubbles
        this.activeBubbles.delete(bubbleId);
        
        // Disconnect observer
        if (this.observers.has(bubbleId)) {
            this.observers.get(bubbleId).disconnect();
            this.observers.delete(bubbleId);
        }
    }
    
    // Public method to destroy the entire system
    destroy() {
        // Cancel all animation frames
        for (const frameId of this.animationFrames.values()) {
            cancelAnimationFrame(frameId);
        }
        
        // Disconnect all observers
        for (const observer of this.observers.values()) {
            observer.disconnect();
        }
        
        // Remove global listeners
        document.removeEventListener('mousemove', this.boundMouseMove);
        document.removeEventListener('mouseup', this.boundMouseUp);
        document.removeEventListener('touchmove', this.boundTouchMove);
        document.removeEventListener('touchend', this.boundTouchEnd);
        
        // Clear all maps
        this.activeBubbles.clear();
        this.animationFrames.clear();
        this.observers.clear();
    }
}

// Global instance
window.bubbleDragSystem = new BubbleDragSystem();

// Enhanced bubble creation function with shape support
function createBubbleWithShape(dialog, emotion, bubbleIndex, offsetX = 0, offsetY = 0) {
    const bubble = document.createElement('div');
    bubble.classList.add('bubble');
    
    // Determine bubble shape based on emotion
    switch (emotion) {
        case 'shout':
        case 'angry':
        case 'yell':
            bubble.classList.add('shout');
            break;
        case 'whisper':
        case 'quiet':
        case 'soft':
            bubble.classList.add('whisper');
            break;
        case 'thought':
        case 'thinking':
        case 'internal':
            bubble.classList.add('thought');
            break;
        case 'dream':
        case 'fantasy':
        case 'imagination':
            bubble.classList.add('dream');
            break;
        case 'electric':
        case 'shock':
        case 'surprise':
            bubble.classList.add('electric');
            break;
        case 'jagged':
            // Keep existing jagged implementation for backwards compatibility
            bubble.style.backgroundImage = `url("/static/comic/assets/jagged.png")`;
            bubble.style.backgroundPosition = 'center center';
            bubble.style.backgroundRepeat = 'no-repeat';
            bubble.style.backgroundSize = 'cover';
            bubble.style.backgroundColor = 'transparent';
            bubble.style.width = '300px';
            bubble.style.height = '120px';
            bubble.style.padding = '25px 35px';
            break;
        default:
            bubble.classList.add('speech-standard');
    }
    
    // Set content and attributes
    bubble.innerHTML = dialog;
    bubble.setAttribute('data-editable', 'true');
    bubble.setAttribute('data-bubble-index', bubbleIndex);
    
    // Set initial position
    bubble.style.transform = `translate3d(${offsetX}px, ${offsetY}px, 0)`;
    
    // Make draggable
    window.bubbleDragSystem.makeBubbleDraggable(bubble, bubbleIndex);
    
    return bubble;
}

// Ultra high-quality image enhancement function
function enhanceImageQuality() {
    // Apply ultra-high quality rendering to all images
    const images = document.querySelectorAll('img, canvas, .grid-item, .bubble');
    
    images.forEach(element => {
        // Force high-quality rendering
        element.style.imageRendering = '-webkit-optimize-contrast';
        element.style.imageRendering = 'crisp-edges';
        
        // Enable hardware acceleration
        element.style.transform = element.style.transform || 'translateZ(0)';
        element.style.webkitBackfaceVisibility = 'hidden';
        element.style.backfaceVisibility = 'hidden';
        
        // Enhanced anti-aliasing
        element.style.webkitFontSmoothing = 'antialiased';
        element.style.mozOsxFontSmoothing = 'grayscale';
        
        // For background images
        if (element.style.backgroundImage) {
            element.style.backgroundSize = 'cover';
            element.style.backgroundPosition = 'center center';
            element.style.backgroundRepeat = 'no-repeat';
        }
    });
    
    // Apply to canvas elements specifically
    const canvases = document.querySelectorAll('canvas');
    canvases.forEach(canvas => {
        const ctx = canvas.getContext('2d');
        if (ctx) {
            // Enable high-quality canvas rendering
            ctx.imageSmoothingEnabled = true;
            ctx.imageSmoothingQuality = 'high';
            
            // Set high DPI scaling
            const dpr = window.devicePixelRatio || 1;
            if (dpr > 1) {
                const rect = canvas.getBoundingClientRect();
                canvas.width = rect.width * dpr;
                canvas.height = rect.height * dpr;
                canvas.style.width = rect.width + 'px';
                canvas.style.height = rect.height + 'px';
                ctx.scale(dpr, dpr);
            }
        }
    });
}

// Auto-enhance quality when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', enhanceImageQuality);
} else {
    enhanceImageQuality();
}

// Re-enhance quality when new content is added
const qualityObserver = new MutationObserver((mutations) => {
    let shouldEnhance = false;
    mutations.forEach((mutation) => {
        if (mutation.addedNodes.length > 0) {
            shouldEnhance = true;
        }
    });
    if (shouldEnhance) {
        setTimeout(enhanceImageQuality, 100);
    }
});

qualityObserver.observe(document.body, {
    childList: true,
    subtree: true
});