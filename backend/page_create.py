from backend.class_def import Page,panel,bubble
import json
import os
import srt

def extract_real_dialogue():
    """Extract real dialogue from subtitle files"""
    subtitle_file = 'test1.srt'
    dialogue_list = []
    
    try:
        if os.path.exists(subtitle_file):
            with open(subtitle_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            subtitles = list(srt.parse(content))
            
            for sub in subtitles:
                if sub.content and sub.content != "((action-scene))":
                    clean_text = sub.content.strip()
                    if clean_text and len(clean_text) > 3:
                        dialogue_list.append(clean_text)
            
            if dialogue_list:
                print(f"✅ Extracted {len(dialogue_list)} real dialogue entries from subtitles")
                return dialogue_list
                
    except Exception as e:
        print(f"⚠️ Could not extract subtitles: {e}")
    
    return []

def generate_meaningful_bubble_content(page_num, panel_num):
    """Generate meaningful bubble content for comics"""
    # Try to get real dialogue first
    real_dialogue = extract_real_dialogue()
    
    if real_dialogue:
        # Calculate index based on page and panel
        dialogue_index = ((page_num - 1) * 4) + (panel_num - 1)
        if dialogue_index < len(real_dialogue):
            return real_dialogue[dialogue_index]
    
    # Fallback to story-appropriate dialogue
    story_dialogues = {
        1: ["Our story begins here!", "Something amazing is happening...", "The adventure starts now!", "What will we discover?"],
        2: ["The plot thickens...", "New challenges await!", "Our heroes face danger!", "The stakes are rising!"],
        3: ["The climax approaches!", "Everything comes together!", "The final battle begins!", "Victory or defeat awaits!"]
    }
    
    # Determine act based on page number
    if page_num <= 4:
        act = 1
    elif page_num <= 8:
        act = 2
    else:
        act = 3
    
    act_dialogues = story_dialogues.get(act, story_dialogues[2])
    
    # Return appropriate dialogue for this panel
    if panel_num <= len(act_dialogues):
        return act_dialogues[panel_num - 1]
    else:
        return "((action-scene))"

def page_create(page_templates,panels,bubbles):
    count = 0
    pages = []
    print(f"Creating pages: {len(page_templates)} templates, {len(panels)} panels, {len(bubbles)} bubbles")
    
    # FORCE EXACTLY 12 PAGES
    max_pages = 12
    
    for i, page_template in enumerate(page_templates):
        # STOP AT 12 PAGES EXACTLY
        if i >= max_pages:
            print(f"🔥 STOPPING AT 12 PAGES: Ignoring remaining {len(page_templates) - i} templates")
            break
            
        try:
            # Ensure we don't go out of bounds
            end_idx = min(count + len(page_template), len(panels))
            panel_slice = panels[count:end_idx]
            bubble_slice = bubbles[count:end_idx] if count < len(bubbles) else []
            
            # Fix existing bubbles that have empty dialogue
            for j, existing_bubble in enumerate(bubble_slice):
                if hasattr(existing_bubble, 'dialog') and (not existing_bubble.dialog or existing_bubble.dialog == ""):
                    existing_bubble.dialog = generate_meaningful_bubble_content(i+1, j+1)
            
            # Pad with unique panels/bubbles if needed
            while len(panel_slice) < len(page_template):
                panel_index = len(panel_slice) + count + 1
                panel_slice.append(panel(f"frame{panel_index:03d}", 1, 1))  # Unique panel
            while len(bubble_slice) < len(page_template):
                # Generate meaningful dialogue instead of empty bubbles
                meaningful_dialogue = generate_meaningful_bubble_content(i+1, len(bubble_slice)+1)
                bubble_slice.append(bubble(50 + len(bubble_slice)*25, 50 + len(bubble_slice)*20, -1, -1, meaningful_dialogue, "normal"))
            
            new_page = Page(panel_slice, bubble_slice)
            pages.append(new_page)
            count = end_idx
            print(f"Page {i+1}: {len(panel_slice)} panels, {len(bubble_slice)} bubbles")
            
        except Exception as e:
            print(f"Error creating page {i+1}: {e}")
            # Create a default page with unique images
            default_panels = [panel(f"frame{j+1:03d}", 1, 1) for j in range(len(page_template))]
            default_bubbles = [bubble(0, 0, -1, -1, "", "normal") for _ in range(len(page_template))]
            new_page = Page(default_panels, default_bubbles)
            pages.append(new_page)

    return pages


def page_json(pages):
    pages_dict = []

    for page in pages:
        pages_dict.append(page.__dict__)

    with open('output_template/page.js', 'w') as f:
        f.write(f'var pages = ')
        json.dump(pages_dict, f , indent=4)
    
    # Generate story summary after creating pages
    try:
        from backend.story_summary import generate_comic_story_summary
        print("🔄 Generating story summary...")
        summary = generate_comic_story_summary()
        if summary:
            print("✅ Story summary generated successfully!")
    except Exception as e:
        print(f"⚠️ Could not generate story summary: {e}")