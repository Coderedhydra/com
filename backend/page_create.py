from backend.class_def import Page,panel,bubble
import json

def page_create(page_templates,panels,bubbles):
    count = 0
    pages = []
    print(f"Creating pages: {len(page_templates)} templates, {len(panels)} panels, {len(bubbles)} bubbles")
    
    for i, page_template in enumerate(page_templates):
        try:
            # Ensure we don't go out of bounds
            end_idx = min(count + len(page_template), len(panels))
            panel_slice = panels[count:end_idx]
            bubble_slice = bubbles[count:end_idx] if count < len(bubbles) else []
            
            # Pad with unique panels/bubbles if needed
            while len(panel_slice) < len(page_template):
                panel_index = len(panel_slice) + count + 1
                panel_slice.append(panel(f"frame{panel_index:03d}", 1, 1))  # Unique panel
            while len(bubble_slice) < len(page_template):
                bubble_slice.append(bubble(0, 0, -1, -1, "", "normal"))  # Default bubble
            
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