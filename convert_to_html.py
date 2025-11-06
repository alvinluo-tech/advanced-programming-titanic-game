import json
import re
from generate_challenge import generate_game_data, save_game_data


def markdown_to_html(md_text):
    """Convert basic markdown to HTML (supports multiple reveal blocks)"""
    html = md_text

    import uuid
    # correction for multiple reveal blocks
    def replace_reveal(m):
        reveal_id = str(uuid.uuid4())[:8]
        return (
            f'<div class="answer-reveal">'
            f'<button class="reveal-btn" onclick="toggleAnswer(\'{reveal_id}\')">Click to Reveal Answer</button>'
            f'<div class="answer-content" id="answer-{reveal_id}" style="display:none;">'
            f'{m.group(1).strip()}</div></div>'
        )

    html = re.sub(
        r'\[\[REVEAL_ANSWER\]\](.*?)\[\[END_REVEAL\]\]',
        replace_reveal,
        html,
        flags=re.DOTALL
    )

    # Markdown → HTML replacements
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)

    # regardless of quotes or spaces
    html = re.sub(
        r'!\[(.+?)\]\((.+?)\)',
        r'<div class="chart-container"><img src="\2" alt="\1" style="max-width:100%;height:auto;border-radius:8px;box-shadow:0 4px 8px rgba(0,0,0,0.1);"></div>',
        html
    )

    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    html = re.sub(r'```([\s\S]+?)```', r'<pre><code>\1</code></pre>', html)
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
    html = re.sub(r'^---', r'<hr>', html, flags=re.MULTILINE)
    html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)

    # Lists
    lines = html.split('\n')
    html_lines, in_list = [], False
    for line in lines:
        if line.strip().startswith('-'):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{line.strip()[1:].strip()}</li>')
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(line)
    if in_list:
        html_lines.append('</ul>')
    html = '\n'.join(html_lines)

    # Paragraphs
    paragraphs = html.split('\n\n')
    html_paragraphs = []
    for para in paragraphs:
        para = para.strip()
        if para and not para.startswith('<') and '</' not in para:
            html_paragraphs.append(f'<p>{para}</p>')
        else:
            html_paragraphs.append(para)
    html = '\n\n'.join(html_paragraphs)
    return html



def format_challenge_1(data):
    """Format Challenge 1 to Markdown"""
    md = f"## {data['title']}\n\n"
    md += f"**Story:** {data['story']}\n\n"
    md += f"**Task:** {data['task']}\n\n"
    
    # Add hint chart if it exists
    if 'hint_chart' in data and data['hint_chart']:
        md += f"![Box Plot]({data['hint_chart']})\n\n"
    
    md += "### Passenger Cards (Show to Players)\n\n"

    fake_card_index = -1
    for i, card in enumerate(data['passenger_cards']):
        md += f"**Card {i + 1}**\n"
        md += "```\n"
        for key, value in card.items():
            if key != "_is_fake":  # Don't show GM marker
                md += f"{key}: {value}\n"
        md += "```\n"

        if card.get("_is_fake"):
            fake_card_index = i + 1

    md += "\n---\n"
    md += "### GM Guide\n\n"
    md += f"> **Hint:** {data['hint']}\n"
    md += f"> **Answer:** [[REVEAL_ANSWER]]{data['answer']} **(In this game, this card is Card {fake_card_index})**[[END_REVEAL]]\n"
    md += "> **Obtain:** **Temporal Coordinate Fragment 1** hidden under the forged card.\n\n"
    return md


def format_challenge_3(data):
    """Format Challenge 3 (Lifeboat Code) to Markdown"""
    md = f"## {data['title']}\n\n"
    md += f"**Story:** {data.get('story', '')}\n\n"
    md += f"**Task:** {data.get('instructions', data.get('task', ''))}\n\n"

    # render hint charts
    if 'hint_chart' in data and data['hint_chart']:
        if isinstance(data['hint_chart'], list):
            for idx, chart_path in enumerate(data['hint_chart']):
                clean_path = str(chart_path).strip().replace("\\", "/").replace("'", "")
                md += f"![Hint Chart {idx + 1}]({clean_path})\n\n"
        else:
            clean_path = str(data['hint_chart']).strip().replace("\\", "/").replace("'", "")
            md += f"![Hint Chart]({clean_path})\n\n"
    elif 'static_clues' in data:
        md += "### Survival Clues\n\n"
        for clue in data['static_clues']:
            md += f"**{clue['heading']}**\n\n{clue['content']}\n\n"

    md += "### Passenger Cards (Show to Players)\n\n"
    for i, card in enumerate(data['passengers']):
        md += f"**Card {i + 1}**\n"
        md += "```\n"
        for key, value in card.items():
            if key != 'Survived':
                md += f"{key}: {value}\n"
        md += "```\n"

    md += "\n---\n"
    md += "### GM Guide\n\n"
    md += f"> **Hint:** Use the survival charts above to infer the 4-digit lifeboat code.\n"
    md += f"> **Answer:** [[REVEAL_ANSWER]]{data['correct_code']}[[END_REVEAL]]\n"
    md += "> **Obtain:** **Temporal Coordinate Fragment 3** hidden within the lifeboat control panel.\n\n"

    return md



def get_html_template():
    """Return HTML template with embedded CSS"""
    # Use raw strings to avoid double escaping
    css = """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .content {
            padding: 40px;
        }
        
        h1 {
            font-size: 2.2em;
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }
        
        h2 {
            font-size: 1.8em;
            color: #764ba2;
            margin: 30px 0 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid #764ba2;
        }
        
        h3 {
            font-size: 1.4em;
            color: #555;
            margin: 20px 0 10px;
        }
        
        h4 {
            font-size: 1.2em;
            color: #666;
            margin: 15px 0 8px;
        }
        
        p {
            margin-bottom: 15px;
            text-align: justify;
        }
        
        strong {
            color: #667eea;
            font-weight: 600;
        }
        
        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', monospace;
            color: #d63384;
        }
        
        pre {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 15px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        pre code {
            background: transparent;
            color: inherit;
            padding: 0;
            border-radius: 0;
        }
        
        blockquote {
            border-left: 4px solid #667eea;
            padding-left: 20px;
            margin: 20px 0;
            background: #f8f9fa;
            padding: 15px 20px;
            border-radius: 5px;
            font-style: italic;
            color: #555;
        }
        
        hr {
            border: none;
            height: 3px;
            background: linear-gradient(to right, #667eea, #764ba2);
            margin: 30px 0;
            border-radius: 2px;
        }
        
        ul {
            margin: 15px 0 15px 30px;
        }
        
        li {
            margin-bottom: 8px;
        }
        
        .card {
            background: #fff;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin: 15px 0;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            border-color: #667eea;
        }
        
        .gm-hint {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }
        
        .answer-box {
            background: #d1ecf1;
            border-left: 4px solid #0dcaf0;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }
        
        .chart-container {
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        
        .chart-container img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
        }
        
        .answer-reveal {
            margin: 20px 0;
        }
        
        .reveal-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 6px;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
        }
        
        .reveal-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
        }
        
        .reveal-btn:active {
            transform: translateY(0);
        }
        
        .answer-content {
            background: #fff9e6 !important;
            color: #000000 !important;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
            animation: fadeIn 0.5s ease-in;
            font-weight: 500;
        }
        
        .answer-content strong {
            color: #d63384 !important;
            font-weight: bold;
        }
        
        /* Crossword Styles */
        #crossword-container {
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        
        .crossword-content {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            align-items: flex-start;
        }
        
        .crossword-grid-wrapper {
            flex: 1;
            min-width: 300px;
        }
        
        table.crossword-grid {
            margin: 20px auto;
            border-collapse: collapse;
            background: white;
        }
        
        table.crossword-grid td {
            width: 35px;
            height: 35px;
            border: 1px solid #ccc;
            text-align: center;
            vertical-align: middle;
            font-weight: bold;
            font-size: 16px;
        }
        
        table.crossword-grid td.filled {
            background: #667eea;
            color: white;
        }
        
        table.crossword-grid td.empty {
            background: #f0f0f0;
        }
        
        .crossword-words-list {
            margin: 20px 0;
            padding: 15px;
            background: #e3f2fd;
            border-radius: 8px;
        }
        
        .crossword-words-list ul {
            list-style: none;
            padding: 0;
        }
        
        .crossword-words-list li {
            padding: 8px;
            margin: 5px 0;
            background: white;
            border-radius: 5px;
        }
        
        .answer-image-container {
            text-align: center;
            margin: 20px 0;
            padding: 15px;
            background: #fff9e6;
            border-radius: 8px;
        }
        
        .answer-image-container img {
            max-width: 800px;
            display: block;
            margin: 0 auto;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .print-btn {
            background: white;
            color: #667eea;
            border: 2px solid white;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s;
            margin-top: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        .print-btn:hover {
            background: #f8f9fa;
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.3);
        }
        
        .print-btn:active {
            transform: translateY(0);
        }
        
        @media print {
            body {
                background: white;
                padding: 0;
            }
            
            .print-btn {
                display: none !important;
            }
            
            .container {
                box-shadow: none;
                max-width: 100%;
            }
            
            .header {
                page-break-after: avoid;
            }
            
            h1, h2, h3 {
                page-break-after: avoid;
            }
            
            pre {
                page-break-inside: avoid;
            }
            
            blockquote {
                page-break-inside: avoid;
            }
            
            /* Reveal all answers in print */
            .answer-content {
                display: block !important;
            }
            
            .reveal-btn {
                display: none !important;
            }
        }
        
        @media (max-width: 768px) {
            .container {
                margin: 10px;
            }
            
            .header h1 {
                font-size: 1.8em;
            }
            
            h2 {
                font-size: 1.5em;
            }
            
            .content {
                padding: 20px;
            }
        }
    """
    
    template_str = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GM Guide - The Temporal Rift on the Titanic</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <style>CssStringPlaceholder</style>
</head>
<body>
    <div class="container" id="guide-container">
        <div class="header">
            <h1>🎮 GM Guide</h1>
            <p style="font-size: 1.2em; margin-top: 10px;">The Temporal Rift on the Titanic</p>
            <button onclick="captureScreenshot()" class="print-btn" id="screenshot-btn">📸 Capture Full Page</button>
        </div>
        <div class="content">
            ContentPlaceholder
        </div>
    </div>
    
    <script>
    function toggleAnswer(id) {
        const answerDiv = document.getElementById('answer-' + id);
        const btn = event.target;
        
        if (answerDiv.style.display === 'none' || answerDiv.style.display === '') {
            answerDiv.style.display = 'block';
            btn.textContent = 'Hide Answer';
            btn.style.background = 'linear-gradient(135deg, #dc3545 0%, #c82333 100%)';
        } else {
            answerDiv.style.display = 'none';
            btn.textContent = 'Click to Reveal Answer';
            btn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        }
    }
    
    // Crossword generation and rendering
    function renderCrossword() {
        const container = document.getElementById('crossword-container');
        if (!container) return;
        
        const wordsJson = container.getAttribute('data-words');
        const gridJson = container.getAttribute('data-grid');
        
        if (!wordsJson) return;
        
        const words = JSON.parse(wordsJson);
        const grid = gridJson ? JSON.parse(gridJson) : null;
        
        let html = '<div class="crossword-content">';
        
        // Render grid if available
        if (grid && grid.length > 0) {
            html += '<div class="crossword-grid-wrapper">';
            html += '<p><strong>Crossword Grid:</strong></p>';
            html += '<table class="crossword-grid">';
            
            // Render the grid - show all cells that contain content
            for (let i = 0; i < grid.length; i++) {
                html += '<tr>';
                for (let j = 0; j < grid[i].length; j++) {
                    const cell = grid[i][j];
                    // Show all cells that have content (filled cells from the grid)
                    if (cell !== '') {
                        // Show as input field for user to fill
                        html += `<td class="crossword-cell" style="background: #fff; border: 2px solid #667eea; width: 40px; height: 40px;"><input type="text" maxlength="1" style="width: 100%; height: 100%; border: none; text-align: center; font-weight: bold; font-size: 18px; text-transform: uppercase; background: #fef3c7;"></td>`;
                    } else {
                        // Empty space (black cell)
                        html += `<td class="crossword-cell" style="background: #333; border: 1px solid #555; width: 40px; height: 40px;"></td>`;
                    }
                }
                html += '</tr>';
            }
            
            html += '</table></div>';
        }
        
        // Word list and clues
        html += '<div class="crossword-words-list"><p><strong>Words to find:</strong></p><ul>';
        words.forEach(word => {
            html += `<li>${word.toUpperCase()} (${word.length} letters)</li>`;
        });
        html += '</ul></div>';
        
        container.innerHTML = html;
    }
    
    // Initialize crossword when page loads
    document.addEventListener('DOMContentLoaded', function() {
        renderCrossword();
    });
    
    async function captureScreenshot() {
        const btn = document.getElementById('screenshot-btn');
        const container = document.getElementById('guide-container');
        
        // Get all answer elements and buttons
        const allAnswers = document.querySelectorAll('.answer-content');
        const allButtons = document.querySelectorAll('.reveal-btn');
        
        // Save original states
        const originalAnswerStates = Array.from(allAnswers).map(el => el.style.display);
        const originalButtonStates = Array.from(allButtons).map(el => el.style.display);
        
        // Show all answers temporarily for screenshot with better visibility
        allAnswers.forEach(el => {
            el.style.display = 'block';
            el.style.opacity = '1';
            el.style.visibility = 'visible';
            el.style.setProperty('background', '#fff9e6', 'important');
            el.style.setProperty('color', '#000000', 'important');
            el.style.setProperty('border-left', '4px solid #ffc107', 'important');
            el.style.setProperty('border', '1px solid #ffc107', 'important');
        });
        allButtons.forEach(el => {
            el.style.display = 'none';
            el.style.opacity = '1';
        });
        
        // Change button text
        btn.textContent = '📸 Capturing...';
        btn.disabled = true;
        
        // Force browser to render changes (longer wait for better rendering)
        await new Promise(resolve => setTimeout(resolve, 500));
        
        try {
            // Use html2canvas to capture the entire container with better options
            const canvas = await html2canvas(container, {
                backgroundColor: null,
                scale: 2,  // Higher quality
                useCORS: true,
                logging: false,
                allowTaint: false,
                removeContainer: false,
                onclone: function(clonedDoc) {
                    // Force all answer content to be visible in the clone with VERY visible colors
                    const clonedAnswers = clonedDoc.querySelectorAll('.answer-content');
                    clonedAnswers.forEach(el => {
                        // Use very visible background and text colors
                        el.style.cssText = 'display: block !important; ' +
                                         'opacity: 1 !important; ' +
                                         'visibility: visible !important; ' +
                                         'background-color: #fef3c7 !important; ' +
                                         'color: #000000 !important; ' +
                                         'border: 2px solid #f59e0b !important; ' +
                                         'font-weight: 600 !important; ' +
                                         'padding: 15px !important; ' +
                                         'margin: 15px 0 !important; ' +
                                         'border-left: 4px solid #f59e0b !important;';
                        
                        // Get all text inside and make it black
                        const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
                        let node;
                        while (node = walker.nextNode()) {
                            node.nodeValue = node.nodeValue;
                        }
                    });
                }
            });
            
            // Convert canvas to image and download
            const imgData = canvas.toDataURL('image/png', 1.0);
            const link = document.createElement('a');
            link.download = 'gm_guide_full_page.png';
            link.href = imgData;
            link.click();
            
            btn.textContent = '✅ Saved!';
            
            // Restore original states
            setTimeout(() => {
                allAnswers.forEach((el, idx) => {
                    el.style.display = originalAnswerStates[idx] || 'none';
                    el.style.opacity = '';
                    el.style.visibility = '';
                });
                allButtons.forEach((el, idx) => {
                    el.style.display = originalButtonStates[idx] || 'block';
                    el.style.opacity = '';
                });
                
                btn.textContent = '📸 Capture Full Page';
                btn.disabled = false;
            }, 2000);
            
        } catch (error) {
            console.error('Screenshot failed:', error);
            btn.textContent = '❌ Error - Retry';
            btn.disabled = false;
            
            // Restore original states on error
            allAnswers.forEach((el, idx) => {
                el.style.display = originalAnswerStates[idx] || 'none';
                el.style.opacity = '';
                el.style.visibility = '';
            });
            allButtons.forEach((el, idx) => {
                el.style.display = originalButtonStates[idx] || 'block';
                el.style.opacity = '';
            });
        }
    }
    </script>
</body>
</html>"""
    
    # Insert CSS
    return template_str.replace('CssStringPlaceholder', css)

def format_challenge_2(data):
    """Format Challenge 2 - Crossword Puzzle"""
    md = f"\n## {data.get('title', 'Challenge 2')}\n\n"
    md += f"{data.get('story', '')}\n\n"
    md += f"**Task:** {data.get('task', '')}\n\n"

    # Get crossword data
    words = data.get('crossword_words', [])
    grid = data.get('crossword_grid', [])
    filled_grid = data.get('crossword_grid_filled', grid)  # Use filled grid for structure
    placed_words = data.get('placed_words', [])
    answer_image = data.get('answer_image', '')

    md += f"<div id='crossword-container' " \
          f"data-words='{json.dumps(words)}' " \
          f"data-grid='{json.dumps(filled_grid)}' " \
          f"data-placed-words='{json.dumps(placed_words)}'>" \
          f"</div>\n\n"

    md += f"**Hint:** {data.get('hint', '')}\n\n"

    # Use answer image if available
    if answer_image:
        answer_text = f"<div class='answer-image-container'><img src='{answer_image}' alt='Crossword Answer' style='max-width: 100%; border: 2px solid #667eea; border-radius: 8px; padding: 10px; background: white;'/></div>"
    else:
        answer_text = data.get('answer', '')

    md += f"[[REVEAL_ANSWER]]{answer_text}[[END_REVEAL]]\n\n"

    return md
def main():
    # Generate fresh game data (regenerates every run)
    game_data = generate_game_data()

    # Save the JSON file for reference
    save_game_data(game_data)
    
    # Start building Markdown
    md_output = f"# {game_data['story_background']['theme']}: GM Guide\n\n"
    md_output += f"**Player Role:** {game_data['story_background']['role']}\n"
    md_output += f"**Final Goal:** {game_data['story_background']['goal']}\n\n"
    md_output += "--- \n"

    # Format function mapping~
    format_functions = [
        format_challenge_1,
        format_challenge_2,
        format_challenge_3
    ]
    print("Converting challenges to Markdown...")
    for i, challenge_data in enumerate(game_data['challenges']):
        md_output += format_functions[i](challenge_data)
        md_output += "---\n"

    md_output += "## Game End\n\n"
    md_output += "Congratulations! You've collected all 5 coordinate fragments, restarted the time machine, and successfully escaped from 1912 at the moment the Titanic sank.\n"
    
    # Save markdown file
    print("Saving Markdown file...")
    with open('gm_guide.md', 'w', encoding='utf-8') as f:
        f.write(md_output)
    print("[OK] gm_guide.md saved")
    
    # Convert markdown to HTML
    print("Converting Markdown to HTML...")
    html_content = markdown_to_html(md_output)
    
    # Wrap in template - replace ContentPlaceholder with actual content
    template = get_html_template()
    html_output = template.replace('ContentPlaceholder', html_content)
    
    # Write to HTML file
    output_filename = 'gm_guide.html'
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(html_output)

    print(f"[OK] {output_filename} saved")
    print("\n[SUCCESS] All guides generated successfully!")
    print("You can open gm_guide.html in your web browser to view the guide.")


if __name__ == "__main__":
    main()

