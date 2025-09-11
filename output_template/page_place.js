path = '/static/comic/frames/final/'
current_page = 0

async function placeDialogs(page) {
    var gridItems = document.querySelectorAll('.grid-item');
    
    // Get story context for this page
    const storyContext = {
        pageNumber: current_page + 1,
        emotion: page.emotion || 'neutral',
        importance: getPageImportance(current_page + 1),
        act: getActForPage(current_page + 1)
    };
    
    // Process each panel with AI enhancement
    for (let index = 0; index < page.panels.length; index++) {
        const panel = page.panels[index];
        const gridItem = gridItems[index];

        gridItem.style.display = 'flex';
        gridItem.style.gridRow = 'span ' + panel.row_span;
        gridItem.style.gridColumn = 'span ' + panel.col_span;
        gridItem.style.backgroundImage = `url("${path}${panel.image}.png")`;

        gridItem.innerHTML = "";

        const dialog_temp = page['bubbles'][index]['dialog'];

        if(dialog_temp != "((action-scene))"){
            // Create AI-enhanced bubble with LLM optimization
            const bubble_temp = createAIBubble(dialog_temp, {
                left: page['bubbles'][index]['bubble_offset_x'] || 91.7906,
                top: page['bubbles'][index]['bubble_offset_y'] || 40.3875,
                maxWidth: 180,
                minHeight: 50,
                fontSize: calculateOptimalFontSize(dialog_temp, storyContext),
                emotion: page['bubbles'][index]['emotion'] || storyContext.emotion,
                bubbleIndex: index
            });

            // Add bubble directly to gridItem, no wrapper
            gridItem.appendChild(bubble_temp);

            // Add event listeners for editing
            addBubbleInteractions(bubble_temp);
        }
        
        // Apply LLM image enhancement to this panel
        if (window.llmEnhancementSystem && window.llmEnhancementSystem.isInitialized) {
            await enhanceGridItemImage(gridItem, storyContext);
        }
    }

    // Hide unused grid items
    for (var i = page.panels.length; i < gridItems.length; i++) {
        gridItems[i].style.display = 'none';
    }
    
    // Apply comprehensive page enhancement
    if (window.llmEnhancementSystem) {
        const pageElement = document.querySelector('.wrapper');
        await window.llmEnhancementSystem.enhanceComicPage(pageElement, current_page + 1, storyContext);
    }
    
    console.log(`📖 Enhanced page ${current_page + 1} with LLM-powered optimizations`);
}

// Helper functions for story optimization
function getPageImportance(pageNumber) {
    // Critical story beats get higher importance
    const criticalPages = [1, 5, 11, 15, 20]; // Opening, inciting incident, midpoint, climax, resolution
    const highPages = [3, 8, 13, 17, 19]; // Character moments, crisis, victory, reflection
    
    if (criticalPages.includes(pageNumber)) return 1.0;
    if (highPages.includes(pageNumber)) return 0.8;
    return 0.6;
}

function getActForPage(pageNumber) {
    if (pageNumber <= 6) return 'act1';
    if (pageNumber <= 10) return 'act2a';
    if (pageNumber <= 14) return 'act2b';
    if (pageNumber <= 17) return 'act3a';
    return 'act3b';
}

function calculateOptimalFontSize(text, context) {
    const baseSize = 12;
    const lengthFactor = Math.max(0.8, Math.min(1.2, 1 - (text.length * 0.01)));
    const importanceFactor = context.importance > 0.8 ? 1.1 : 1.0;
    const emotionFactor = ['action', 'triumph', 'shock'].includes(context.emotion) ? 1.15 : 1.0;
    
    return Math.round(baseSize * lengthFactor * importanceFactor * emotionFactor);
}

async function enhanceGridItemImage(gridItem, context) {
    try {
        // Create a temporary image from background
        const bgImage = gridItem.style.backgroundImage;
        if (!bgImage || bgImage === 'none') return;
        
        const imageUrl = bgImage.slice(4, -1).replace(/"/g, '');
        const img = new Image();
        
        img.onload = async function() {
            try {
                // Apply LLM-powered image enhancement
                const enhanced = await window.llmEnhancementSystem.enhanceImageQuality(img, {
                    upscaleFactor: context.importance > 0.8 ? 3 : 2,
                    sharpnessBoost: context.importance > 0.7 ? 1.4 : 1.2,
                    denoiseStrength: 0.7,
                    useGPU: true
                });
                
                // Apply emotion-based color enhancement
                const colorEnhanced = await window.llmEnhancementSystem.upgradeColors(enhanced, context.emotion);
                
                // Update the grid item background
                gridItem.style.backgroundImage = `url(${colorEnhanced.src})`;
                gridItem.classList.add('llm-enhanced');
                
            } catch (error) {
                console.warn('Failed to enhance grid item image:', error);
            }
        };
        
        img.crossOrigin = 'anonymous';
        img.src = imageUrl;
        
    } catch (error) {
        console.warn('Error in grid item enhancement:', error);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    placeDialogs(pages[current_page]);
    
    // Only bubbles should be draggable, not panels
    // Template should remain fixed at 800x540
});

function prevPage(){
    current_page = (current_page - 1);
    if(current_page < 0){
        current_page = pages.length - 1;
    }
    placeDialogs(pages[current_page]);
}

function nextPage(){
    current_page = (current_page + 1) % pages.length;
    placeDialogs(pages[current_page]);
}

// Bubble interaction functions
function addBubbleInteractions(bubble) {
    let isDragging = false;
    let isEditing = false;
    let startX, startY, initialX, initialY;

    // Double-tap to edit
    let tapCount = 0;
    bubble.addEventListener('click', function(e) {
        tapCount++;
        setTimeout(() => {
            if (tapCount === 2) {
                editBubble(bubble);
            }
            tapCount = 0;
        }, 300);
    });

    // Drag functionality
    bubble.addEventListener('mousedown', function(e) {
        if (isEditing) return;
        isDragging = true;
        startX = e.clientX;
        startY = e.clientY;
        
        const transform = bubble.style.transform;
        const matches = transform.match(/translate\(([^,]+)px,\s*([^)]+)px\)/);
        if (matches) {
            initialX = parseFloat(matches[1]);
            initialY = parseFloat(matches[2]);
        } else {
            initialX = 0;
            initialY = 0;
        }
        
        bubble.style.cursor = 'grabbing';
        e.preventDefault();
    });

    document.addEventListener('mousemove', function(e) {
        if (!isDragging) return;
        
        const deltaX = e.clientX - startX;
        const deltaY = e.clientY - startY;
        
        bubble.style.transform = `translate(${initialX + deltaX}px, ${initialY + deltaY}px)`;
    });

    document.addEventListener('mouseup', function() {
        if (isDragging) {
            isDragging = false;
            bubble.style.cursor = 'grab';
        }
    });

    // Touch events for mobile
    bubble.addEventListener('touchstart', function(e) {
        if (isEditing) return;
        isDragging = true;
        startX = e.touches[0].clientX;
        startY = e.touches[0].clientY;
        
        const transform = bubble.style.transform;
        const matches = transform.match(/translate\(([^,]+)px,\s*([^)]+)px\)/);
        if (matches) {
            initialX = parseFloat(matches[1]);
            initialY = parseFloat(matches[2]);
        } else {
            initialX = 0;
            initialY = 0;
        }
        
        e.preventDefault();
    });

    document.addEventListener('touchmove', function(e) {
        if (!isDragging) return;
        
        const deltaX = e.touches[0].clientX - startX;
        const deltaY = e.touches[0].clientY - startY;
        
        bubble.style.transform = `translate(${initialX + deltaX}px, ${initialY + deltaY}px)`;
        e.preventDefault();
    });

    document.addEventListener('touchend', function() {
        isDragging = false;
    });
}

function editBubble(bubble) {
    const originalText = bubble.innerHTML;
    const input = document.createElement('input');
    input.type = 'text';
    input.value = originalText;
    input.style.width = '100%';
    input.style.height = '100%';
    input.style.border = 'none';
    input.style.background = 'transparent';
    input.style.fontSize = bubble.style.fontSize;
    input.style.fontFamily = bubble.style.fontFamily;
    input.style.textAlign = 'center';
    input.style.outline = 'none';
    
    bubble.innerHTML = '';
    bubble.appendChild(input);
    input.focus();
    input.select();
    
    input.addEventListener('blur', function() {
        bubble.innerHTML = input.value;
    });
    
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            bubble.innerHTML = input.value;
        }
    });
}

// Print/Download functionality
function printPage() {
    console.log('Starting print function...');
    
    // Check if html2canvas is loaded
    if (typeof html2canvas === 'undefined') {
        // Fallback to browser print
        console.log('html2canvas not available, using browser print...');
        alert('Using browser print function. Make sure to select "Save as PDF" or print to file.');
        window.print();
        return;
    }
    
    const wrapper = document.querySelector('.wrapper');
    if (!wrapper) {
        alert('No content to print.');
        return;
    }
    
    // Create a temporary container with the page content
    const tempContainer = document.createElement('div');
    tempContainer.style.width = '800px';
    tempContainer.style.height = '1080px';
    tempContainer.style.position = 'absolute';
    tempContainer.style.left = '-9999px';
    tempContainer.style.top = '0';
    tempContainer.style.backgroundColor = 'white';
    tempContainer.style.overflow = 'hidden';
    
    // Clone the wrapper content
    const clonedContent = wrapper.cloneNode(true);
    clonedContent.style.width = '800px';
    clonedContent.style.height = '1080px';
    clonedContent.style.margin = '0';
    clonedContent.style.padding = '0';
    
    tempContainer.appendChild(clonedContent);
    document.body.appendChild(tempContainer);
    
    console.log('Capturing page with html2canvas...');
    
    // Use html2canvas to capture the page
    html2canvas(tempContainer, {
        width: 800,
        height: 1080,
        scale: 1,
        useCORS: true,
        allowTaint: true,
        backgroundColor: '#ffffff',
        logging: true,
        onclone: function(clonedDoc) {
            console.log('Canvas cloned successfully');
        }
    }).then(canvas => {
        console.log('Canvas created, downloading...');
        
        // Download the canvas as PNG
        const link = document.createElement('a');
        link.download = `comic_page_${current_page + 1}_800x1080.png`;
        link.href = canvas.toDataURL('image/png', 1.0);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        console.log('Download started');
        
        // Clean up
        document.body.removeChild(tempContainer);
    }).catch(error => {
        console.error('Error generating image:', error);
        alert('Error generating image: ' + error.message);
        if (document.body.contains(tempContainer)) {
            document.body.removeChild(tempContainer);
        }
    });
}

function printAllPages() {
    const originalPage = current_page;
    let pageIndex = 0;
    
    function printNextPage() {
        if (pageIndex < pages.length) {
            current_page = pageIndex;
            placeDialogs(pages[current_page]);
            
            setTimeout(() => {
                printPage();
                pageIndex++;
                setTimeout(printNextPage, 1000); // Wait 1 second between pages
            }, 500); // Wait for page to render
        } else {
            // Restore original page
            current_page = originalPage;
            placeDialogs(pages[current_page]);
        }
    }
    
    printNextPage();
}

// Image upload and manipulation functions
function uploadImage() {
    document.getElementById('imageUpload').click();
}

function handleImageUpload(event) {
    const file = event.target.files[0];
    if (file) {
        // Validate file type
        if (!file.type.startsWith('image/')) {
            alert('Please select an image file.');
            return;
        }
        
        // Validate file size (max 10MB)
        if (file.size > 10 * 1024 * 1024) {
            alert('File size too large. Please select an image smaller than 10MB.');
            return;
        }
        
        const reader = new FileReader();
        reader.onload = function(e) {
            const imageUrl = e.target.result;
            // Ask user which panel to replace with better UI
            const panelChoice = prompt('Which panel to replace?\n\n1 - Top panel\n2 - Bottom panel\n\nEnter 1 or 2:');
            if (panelChoice === '1' || panelChoice === '2') {
                replacePanelImage(panelChoice, imageUrl);
                alert(`Panel ${panelChoice} image updated successfully!`);
            } else if (panelChoice !== null) {
                alert('Invalid choice. Please enter 1 or 2.');
            }
        };
        reader.onerror = function() {
            alert('Error reading file. Please try again.');
        };
        reader.readAsDataURL(file);
    }
}

function replacePanelImage(panelNumber, imageUrl) {
    const panel = document.getElementById(`_${panelNumber}`);
    if (panel) {
        panel.style.backgroundImage = `url("${imageUrl}")`;
        panel.style.backgroundSize = 'contain';
        panel.style.backgroundPosition = 'center';
        panel.style.backgroundRepeat = 'no-repeat';
        
        // Add image controls
        addImageControls(panel, imageUrl);
    }
}

function addImageControls(panel, imageUrl) {
    // Remove existing controls if any
    const existingControls = panel.querySelector('.image-controls');
    if (existingControls) {
        existingControls.remove();
    }
    
    // Create control panel
    const controls = document.createElement('div');
    controls.className = 'image-controls';
    controls.style.position = 'absolute';
    controls.style.top = '5px';
    controls.style.right = '5px';
    controls.style.zIndex = '10';
    controls.style.backgroundColor = 'rgba(0,0,0,0.7)';
    controls.style.padding = '5px';
    controls.style.borderRadius = '3px';
    
    // Zoom controls
    const zoomInBtn = document.createElement('button');
    zoomInBtn.innerHTML = '+';
    zoomInBtn.style.margin = '2px';
    zoomInBtn.style.padding = '2px 6px';
    zoomInBtn.style.backgroundColor = 'white';
    zoomInBtn.style.border = '1px solid #ccc';
    zoomInBtn.style.borderRadius = '2px';
    zoomInBtn.style.cursor = 'pointer';
    zoomInBtn.onclick = () => zoomImage(panel, 1.2);
    
    const zoomOutBtn = document.createElement('button');
    zoomOutBtn.innerHTML = '-';
    zoomOutBtn.style.margin = '2px';
    zoomOutBtn.style.padding = '2px 6px';
    zoomOutBtn.style.backgroundColor = 'white';
    zoomOutBtn.style.border = '1px solid #ccc';
    zoomOutBtn.style.borderRadius = '2px';
    zoomOutBtn.style.cursor = 'pointer';
    zoomOutBtn.onclick = () => zoomImage(panel, 0.8);
    
    const resetBtn = document.createElement('button');
    resetBtn.innerHTML = '↺';
    resetBtn.style.margin = '2px';
    resetBtn.style.padding = '2px 6px';
    resetBtn.style.backgroundColor = 'white';
    resetBtn.style.border = '1px solid #ccc';
    resetBtn.style.borderRadius = '2px';
    resetBtn.style.cursor = 'pointer';
    resetBtn.onclick = () => resetImage(panel);
    
    controls.appendChild(zoomInBtn);
    controls.appendChild(zoomOutBtn);
    controls.appendChild(resetBtn);
    
    panel.appendChild(controls);
    
    // Panels should not be draggable - only bubbles should be draggable
}

function zoomImage(panel, factor) {
    const currentSize = panel.style.backgroundSize || 'contain';
    let currentScale = 1;
    
    if (currentSize.includes('scale')) {
        const match = currentSize.match(/scale\(([0-9.]+)\)/);
        if (match) {
            currentScale = parseFloat(match[1]);
        }
    }
    
    const newScale = currentScale * factor;
    panel.style.backgroundSize = `scale(${newScale})`;
}

function resetImage(panel) {
    panel.style.backgroundSize = 'contain';
    panel.style.backgroundPosition = 'center';
    panel.style.transform = 'translate(0px, 0px)';
}

// Function to make bubbles draggable - only bubbles should be draggable
function makeBubbleDraggable(bubble, bubbleIndex) {
    let isDragging = false;
    let startX, startY, initialX, initialY;
    
    bubble.addEventListener('mousedown', function(e) {
        isDragging = true;
        startX = e.clientX;
        startY = e.clientY;
        
        // Get current position
        const transform = bubble.style.transform;
        const matches = transform.match(/translate\(([^,]+)px,\s*([^)]+)px\)/);
        if (matches) {
            initialX = parseFloat(matches[1]);
            initialY = parseFloat(matches[2]);
        } else {
            initialX = 0;
            initialY = 0;
        }
        
        e.preventDefault();
        bubble.style.cursor = 'grabbing';
    });
    
    document.addEventListener('mousemove', function(e) {
        if (!isDragging) return;
        
        const deltaX = e.clientX - startX;
        const deltaY = e.clientY - startY;
        
        bubble.style.transform = `translate(${initialX + deltaX}px, ${initialY + deltaY}px)`;
        e.preventDefault();
    });
    
    document.addEventListener('mouseup', function() {
        if (isDragging) {
            isDragging = false;
            bubble.style.cursor = 'move';
            
            // Update the bubble position in the pages data
            if (pages[current_page] && pages[current_page].bubbles[bubbleIndex]) {
                pages[current_page].bubbles[bubbleIndex].bubble_offset_x = initialX + (event.clientX - startX);
                pages[current_page].bubbles[bubbleIndex].bubble_offset_y = initialY + (event.clientY - startY);
            }
        }
    });
    
    // Touch support
    bubble.addEventListener('touchstart', function(e) {
        isDragging = true;
        startX = e.touches[0].clientX;
        startY = e.touches[0].clientY;
        
        const transform = bubble.style.transform;
        const matches = transform.match(/translate\(([^,]+)px,\s*([^)]+)px\)/);
        if (matches) {
            initialX = parseFloat(matches[1]);
            initialY = parseFloat(matches[2]);
        } else {
            initialX = 0;
            initialY = 0;
        }
        
        e.preventDefault();
    });
    
    document.addEventListener('touchmove', function(e) {
        if (!isDragging) return;
        
        const deltaX = e.touches[0].clientX - startX;
        const deltaY = e.touches[0].clientY - startY;
        
        bubble.style.transform = `translate(${initialX + deltaX}px, ${initialY + deltaY}px)`;
        e.preventDefault();
    });
    
    document.addEventListener('touchend', function() {
        if (isDragging) {
            isDragging = false;
            
            // Update the bubble position in the pages data
            if (pages[current_page] && pages[current_page].bubbles[bubbleIndex]) {
                pages[current_page].bubbles[bubbleIndex].bubble_offset_x = initialX + (event.changedTouches[0].clientX - startX);
                pages[current_page].bubbles[bubbleIndex].bubble_offset_y = initialY + (event.changedTouches[0].clientY - startY);
            }
        }
    });
}

