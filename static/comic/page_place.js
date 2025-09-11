path = '/static/comic/frames/final/'
current_page = 0

function placeDialogs(page) {
    var gridItems = document.querySelectorAll('.grid-item');
    page.panels.forEach(function (panel, index) {
        var gridItem = gridItems[index];

        gridItem.style.display = 'flex';
        gridItem.style.gridRow = 'span ' + panel.row_span;
        gridItem.style.gridColumn = 'span ' + panel.col_span;
        gridItem.style.backgroundImage = `url("${path}${panel.image}.png")`;

        gridItem.innerHTML = "";

        const dialog_temp = page['bubbles'][index]['dialog'];

        if(dialog_temp != "((action-scene))"){

            // Create advanced bubble with authentic shape
            const bubble_temp = createBubbleWithShape(
                page['bubbles'][index]['dialog'],
                page['bubbles'][index]['emotion'],
                index,
                page['bubbles'][index]['bubble_offset_x'],
                page['bubbles'][index]['bubble_offset_y']
            );

            // Adjust font size based on content length
            const fontSize = Math.max(12, Math.min(20, dialog_temp.length * 0.4));
            bubble_temp.style.fontSize = fontSize + 'px';

            // Add bubble directly to gridItem, no wrapper
            gridItem.appendChild(bubble_temp);

            // Add event listeners for editing
            addBubbleInteractions(bubble_temp);
        }
    });

    for (var i = page.panels.length; i < gridItems.length; i++) {
        gridItems[i].style.display = 'none';
    }
    
    // Ensure perfect image fitting after placing dialogs
    ensurePerfectImageFit();
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

// High-Quality Print/Download functionality
function printPage() {
    console.log('Starting high-quality print function...');
    
    // Check if html2canvas is loaded
    if (typeof html2canvas === 'undefined') {
        console.log('html2canvas not available, loading dynamically...');
        loadHtml2Canvas().then(() => printPage());
        return;
    }
    
    const wrapper = document.querySelector('.wrapper');
    if (!wrapper) {
        alert('No content to print.');
        return;
    }
    
    // Create a high-quality temporary container
    const tempContainer = document.createElement('div');
    tempContainer.style.width = '800px';
    tempContainer.style.height = '1080px';
    tempContainer.style.position = 'absolute';
    tempContainer.style.left = '-9999px';
    tempContainer.style.top = '0';
    tempContainer.style.backgroundColor = '#ffffff';
    tempContainer.style.overflow = 'hidden';
    tempContainer.style.transform = 'scale(1)';
    tempContainer.style.transformOrigin = 'top left';
    
    // Clone the wrapper content with high fidelity
    const clonedContent = wrapper.cloneNode(true);
    clonedContent.style.width = '800px';
    clonedContent.style.height = '1080px';
    clonedContent.style.margin = '0';
    clonedContent.style.padding = '0';
    clonedContent.style.borderRadius = '0';
    clonedContent.style.boxShadow = 'none';
    
    // Ensure all images are loaded and high quality
    const images = clonedContent.querySelectorAll('*');
    images.forEach(element => {
        if (element.style.backgroundImage) {
            element.style.imageRendering = 'high-quality';
            element.style.imageRendering = '-webkit-optimize-contrast';
            element.style.imageRendering = 'crisp-edges';
        }
    });
    
    tempContainer.appendChild(clonedContent);
    document.body.appendChild(tempContainer);
    
    console.log('Capturing page with high-quality settings...');
    
    // Use html2canvas with maximum quality settings
    html2canvas(tempContainer, {
        width: 800,
        height: 1080,
        scale: 3, // 3x scaling for ultra-high quality
        useCORS: true,
        allowTaint: true,
        backgroundColor: '#ffffff',
        logging: false,
        imageTimeout: 30000,
        removeContainer: false,
        foreignObjectRendering: true,
        scrollX: 0,
        scrollY: 0,
        windowWidth: 800,
        windowHeight: 1080,
        onclone: function(clonedDoc) {
            console.log('High-quality canvas cloned successfully');
            // Enhance image quality in cloned document
            const clonedImages = clonedDoc.querySelectorAll('*');
            clonedImages.forEach(element => {
                if (element.style && element.style.backgroundImage) {
                    element.style.imageRendering = 'high-quality';
                    element.style.imageRendering = '-webkit-optimize-contrast';
                }
            });
        }
    }).then(canvas => {
        console.log('High-quality canvas created, processing...');
        
        // Create high-quality PNG with maximum settings
        const highQualityDataURL = canvas.toDataURL('image/png', 1.0);
        
        // Download the high-quality image
        const link = document.createElement('a');
        link.download = `comic_page_${current_page + 1}_HQ_${canvas.width}x${canvas.height}.png`;
        link.href = highQualityDataURL;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        console.log(`High-quality download started: ${canvas.width}x${canvas.height}px`);
        
        // Clean up
        document.body.removeChild(tempContainer);
    }).catch(error => {
        console.error('Error generating high-quality image:', error);
        alert('Error generating high-quality image: ' + error.message + '\nTrying fallback method...');
        
        // Fallback to browser print
        window.print();
        
        if (document.body.contains(tempContainer)) {
            document.body.removeChild(tempContainer);
        }
    });
}

// Function to dynamically load html2canvas if not available
function loadHtml2Canvas() {
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js';
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
    });
}

// Server-side ultra high-quality export
function exportServerSideHQ() {
    console.log('Starting server-side ultra high-quality export...');
    
    const exportButton = document.querySelector('button[onclick="exportServerSideHQ()"]');
    const originalText = exportButton.innerHTML;
    exportButton.innerHTML = 'Exporting...';
    exportButton.disabled = true;
    
    fetch('/export_hq_png', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            page: current_page
        })
    })
    .then(response => {
        if (response.ok) {
            // Server-side export successful - download the file
            return response.blob();
        } else {
            // Fallback to client-side
            return response.json().then(data => {
                console.log('Server-side export not available, using enhanced client-side method');
                printPage(); // Use the enhanced client-side method
                throw new Error('Fallback to client-side');
            });
        }
    })
    .then(blob => {
        if (blob) {
            // Download the server-generated high-quality PNG
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `comic_page_${current_page + 1}_ULTRA_HQ.png`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
            
            console.log('Ultra high-quality server-side export completed');
        }
    })
    .catch(error => {
        console.log('Using client-side high-quality export as fallback');
        // The client-side method is already called above
    })
    .finally(() => {
        // Reset button
        exportButton.innerHTML = originalText;
        exportButton.disabled = false;
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
        panel.style.backgroundSize = 'cover';
        panel.style.backgroundPosition = 'center center';
        panel.style.backgroundRepeat = 'no-repeat';
        panel.style.objectFit = 'cover';
        
        // Ensure perfect fitting with 0% gap for any image size
        panel.style.display = 'flex';
        panel.style.alignItems = 'center';
        panel.style.justifyContent = 'center';
        panel.style.width = '800px';
        panel.style.height = '540px';
        
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
    
    // Panel should not be draggable - only bubbles should be draggable
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
    panel.style.backgroundSize = 'cover';
    panel.style.backgroundPosition = 'center center';
    panel.style.transform = 'translate(0px, 0px)';
}

// Panel dragging removed - only bubbles should be draggable
// Template should remain fixed at 800x540 dimensions



// Function to make bubbles draggable
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

// ULTRA HIGH PERFORMANCE BUBBLE DRAGGING SYSTEM V2
function makeBubbleDraggableUltra(bubble, bubbleIndex) {
    let isDragging = false;
    let startX, startY, initialX, initialY;
    let animationFrame = null;
    let dragThreshold = 3;
    let hasMoved = false;
    
    function getTransformValues(element) {
        const transform = element.style.transform || '';
        const matches = transform.match(/translate(?:3d)?\(([^,]+)(?:px)?(?:,\s*([^,]+)(?:px)?)?(?:,\s*([^)]+)(?:px)?)?\)/);
        if (matches) {
            return {
                x: parseFloat(matches[1]) || 0,
                y: parseFloat(matches[2]) || 0
            };
        }
        return { x: 0, y: 0 };
    }
    
    function updateTransform(x, y) {
        if (animationFrame) cancelAnimationFrame(animationFrame);
        animationFrame = requestAnimationFrame(() => {
            bubble.style.transform = `translate3d(${x}px, ${y}px, 0)`;
        });
    }
    
    bubble.addEventListener('mousedown', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        isDragging = false;
        hasMoved = false;
        startX = e.clientX;
        startY = e.clientY;
        
        const currentPos = getTransformValues(bubble);
        initialX = currentPos.x;
        initialY = currentPos.y;
        
        bubble.classList.add('dragging');
        bubble.style.cursor = 'grabbing';
        bubble.style.zIndex = '2000';
        document.body.style.userSelect = 'none';
    });
    
    document.addEventListener('mousemove', function(e) {
        if (!bubble.classList.contains('dragging')) return;
        
        const deltaX = e.clientX - startX;
        const deltaY = e.clientY - startY;
        
        if (!isDragging && (Math.abs(deltaX) > dragThreshold || Math.abs(deltaY) > dragThreshold)) {
            isDragging = true;
            hasMoved = true;
        }
        
        if (isDragging) {
            e.preventDefault();
            e.stopPropagation();
            updateTransform(initialX + deltaX, initialY + deltaY);
        }
    });
    
    document.addEventListener('mouseup', function(e) {
        if (bubble.classList.contains('dragging')) {
            bubble.classList.remove('dragging');
            bubble.style.cursor = 'grab';
            bubble.style.zIndex = '1000';
            document.body.style.userSelect = '';
            
            if (isDragging && hasMoved) {
                const deltaX = e.clientX - startX;
                const deltaY = e.clientY - startY;
                const finalX = initialX + deltaX;
                const finalY = initialY + deltaY;
                
                if (pages[current_page] && pages[current_page].bubbles[bubbleIndex]) {
                    pages[current_page].bubbles[bubbleIndex].bubble_offset_x = finalX;
                    pages[current_page].bubbles[bubbleIndex].bubble_offset_y = finalY;
                }
            }
            
            isDragging = false;
            hasMoved = false;
        }
    });
    
    // Touch events
    bubble.addEventListener('touchstart', function(e) {
        e.preventDefault();
        const touch = e.touches[0];
        isDragging = false;
        hasMoved = false;
        startX = touch.clientX;
        startY = touch.clientY;
        
        const currentPos = getTransformValues(bubble);
        initialX = currentPos.x;
        initialY = currentPos.y;
        
        bubble.classList.add('dragging');
        bubble.style.zIndex = '2000';
    }, { passive: false });
    
    document.addEventListener('touchmove', function(e) {
        if (!bubble.classList.contains('dragging')) return;
        e.preventDefault();
        
        const touch = e.touches[0];
        const deltaX = touch.clientX - startX;
        const deltaY = touch.clientY - startY;
        
        if (!isDragging && (Math.abs(deltaX) > dragThreshold || Math.abs(deltaY) > dragThreshold)) {
            isDragging = true;
            hasMoved = true;
        }
        
        if (isDragging) {
            updateTransform(initialX + deltaX, initialY + deltaY);
        }
    }, { passive: false });
    
    document.addEventListener('touchend', function(e) {
        if (bubble.classList.contains('dragging')) {
            bubble.classList.remove('dragging');
            bubble.style.zIndex = '1000';
            
            if (isDragging && hasMoved) {
                const touch = e.changedTouches[0];
                const deltaX = touch.clientX - startX;
                const deltaY = touch.clientY - startY;
                const finalX = initialX + deltaX;
                const finalY = initialY + deltaY;
                
                if (pages[current_page] && pages[current_page].bubbles[bubbleIndex]) {
                    pages[current_page].bubbles[bubbleIndex].bubble_offset_x = finalX;
                    pages[current_page].bubbles[bubbleIndex].bubble_offset_y = finalY;
                }
            }
            
            isDragging = false;
            hasMoved = false;
        }
    });
}

// Function to ensure perfect image fitting with 0% gap
function ensurePerfectImageFit() {
    const gridItems = document.querySelectorAll('.grid-item');
    gridItems.forEach(function(item) {
        // Ensure the image fills the entire 800x540 template with 0% gap
        item.style.backgroundSize = 'cover';
        item.style.backgroundPosition = 'center center';
        item.style.backgroundRepeat = 'no-repeat';
        
        // Ensure the container dimensions are exactly 800x540
        item.style.width = '800px';
        item.style.height = '540px';
        item.style.overflow = 'hidden';
        
        // Add a fallback background color
        if (!item.style.backgroundImage || item.style.backgroundImage === 'none') {
            item.style.backgroundColor = '#f0f0f0';
        }
    });
}