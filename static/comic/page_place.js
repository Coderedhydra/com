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

            const wrapper = document.createElement('div');
            wrapper.style.position = 'relative'; // Wrapper to contain the bubble
            wrapper.style.width = '100%';
            wrapper.style.height = '100%';

            const bubble_temp = document.createElement('div');
            bubble_temp.classList.add('bubble');
            bubble_temp.innerHTML = page['bubbles'][index]['dialog'];
            bubble_temp.setAttribute('data-editable', 'true');
            bubble_temp.setAttribute('draggable', 'true');

            const emotion = page['bubbles'][index]['emotion'];

            if (emotion == 'jagged') {
                bubble_temp.style.backgroundImage = `url("assets/jagged.png")`;
                bubble_temp.style.backgroundPosition = 'center center';
                bubble_temp.style.backgroundRepeat = 'no-repeat';
                bubble_temp.style.backgroundSize = 'cover';
                bubble_temp.style.backgroundColor = 'transparent';
                bubble_temp.style.width = '200px';
                bubble_temp.style.height = '94px';
                bubble_temp.style.padding = '70px';
            }

            bubble_temp.style.fontSize = Math.max(12, Math.min(24, dialog_temp.length * 0.5)) + 'px';
            bubble_temp.style.transform = `translate(${page['bubbles'][index]['bubble_offset_x']}px, ${page['bubbles'][index]['bubble_offset_y']}px)`;

            const tail = document.createElement('div');
            tail.classList.add('tail');
            if (page['bubbles'][index]['tail_offset_x'] == null || emotion == 'jagged') {
                tail.style.display = 'none';
            } else {
                tail.style.transform = `translate(${page['bubbles'][index]['tail_offset_x']}px, ${page['bubbles'][index]['tail_offset_y']}px) rotate(${page['bubbles'][index]['tail_deg']}deg)`;
            }

            bubble_temp.appendChild(tail);
            wrapper.appendChild(bubble_temp);
            gridItem.appendChild(wrapper);

            // Add event listeners for editing and dragging
            addBubbleInteractions(bubble_temp);
        }
    });

    for (var i = page.panels.length; i < gridItems.length; i++) {
        gridItems[i].style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    placeDialogs(pages[current_page]);
    
    // Make existing panels draggable
    setTimeout(() => {
        const panels = document.querySelectorAll('.grid-item');
        panels.forEach(panel => {
            if (panel.style.backgroundImage && panel.style.backgroundImage !== 'none') {
                makePanelDraggable(panel);
            }
        });
    }, 1000);
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
                if (pageIndex < pages.length) {
                    setTimeout(printNextPage, 2000); // Wait 2 seconds between pages
                } else {
                    // Restore original page after all pages are printed
                    setTimeout(() => {
                        current_page = originalPage;
                        placeDialogs(pages[current_page]);
                        console.log(`All pages printed! Restored to page ${originalPage + 1}`);
                    }, 1000);
                }
            }, 1000); // Wait for page to render
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
        panel.style.backgroundSize = 'contain'; // Changed to contain for perfect fit without cropping
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
    
    const fitBtn = document.createElement('button');
    fitBtn.innerHTML = 'Fit';
    fitBtn.style.margin = '2px';
    fitBtn.style.padding = '2px 6px';
    fitBtn.style.backgroundColor = 'white';
    fitBtn.style.border = '1px solid #ccc';
    fitBtn.style.borderRadius = '2px';
    fitBtn.style.cursor = 'pointer';
    fitBtn.onclick = () => fitImage(panel);
    
    controls.appendChild(zoomInBtn);
    controls.appendChild(zoomOutBtn);
    controls.appendChild(fitBtn);
    controls.appendChild(resetBtn);
    
    panel.appendChild(controls);
    
    // Make panel draggable
    makePanelDraggable(panel);
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
    
    const newScale = Math.max(0.5, Math.min(3.0, currentScale * factor)); // Limit zoom range
    panel.style.backgroundSize = `scale(${newScale})`;
}

function resetImage(panel) {
    panel.style.backgroundSize = 'contain'; // Changed to contain for perfect fit
    panel.style.backgroundPosition = 'center';
    panel.style.transform = 'translate(0px, 0px)';
}

function fitImage(panel) {
    // Toggle between cover and contain for different fitting options
    const currentSize = panel.style.backgroundSize || 'contain';
    if (currentSize.includes('contain')) {
        panel.style.backgroundSize = 'cover';
    } else {
        panel.style.backgroundSize = 'contain';
    }
    panel.style.backgroundPosition = 'center';
}

function makePanelDraggable(panel) {
    let isDragging = false;
    let startX, startY, initialX, initialY;
    
    panel.addEventListener('mousedown', function(e) {
        if (e.target.tagName === 'BUTTON') return; // Don't drag when clicking buttons
        
        isDragging = true;
        startX = e.clientX;
        startY = e.clientY;
        
        const transform = panel.style.transform;
        const matches = transform.match(/translate\(([^,]+)px,\s*([^)]+)px\)/);
        if (matches) {
            initialX = parseFloat(matches[1]);
            initialY = parseFloat(matches[2]);
        } else {
            initialX = 0;
            initialY = 0;
        }
        
        panel.style.cursor = 'grabbing';
        e.preventDefault();
    });
    
    document.addEventListener('mousemove', function(e) {
        if (!isDragging) return;
        
        const deltaX = e.clientX - startX;
        const deltaY = e.clientY - startY;
        
        panel.style.transform = `translate(${initialX + deltaX}px, ${initialY + deltaY}px)`;
    });
    
    document.addEventListener('mouseup', function() {
        if (isDragging) {
            isDragging = false;
            panel.style.cursor = 'grab';
        }
    });
    
    // Touch events for mobile
    panel.addEventListener('touchstart', function(e) {
        if (e.target.tagName === 'BUTTON') return;
        
        isDragging = true;
        startX = e.touches[0].clientX;
        startY = e.touches[0].clientY;
        
        const transform = panel.style.transform;
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
        
        panel.style.transform = `translate(${initialX + deltaX}px, ${initialY + deltaY}px)`;
        e.preventDefault();
    });
    
    document.addEventListener('touchend', function() {
        isDragging = false;
    });
}

