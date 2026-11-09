from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt


env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "en")  


data_dir = os.path.abspath("Data")
os.makedirs(data_dir, exist_ok=True)


html_file_path = os.path.join(data_dir, "Voice.html")
HtmlCode = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {{
            recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = "{InputLanguage}";
            recognition.continuous = true;

            recognition.onresult = function(event) {{
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript + " ";
            }};

            recognition.onend = function() {{
                recognition.start();
            }};
            recognition.start();
        }}

        function stopRecognition() {{
            recognition.stop();
            output.innerHTML = "";
        }}
    </script>
</body>
</html>
'''
with open(html_file_path, "w", encoding="utf-8") as f:
    f.write(HtmlCode)


file_url = f"file://{html_file_path}"


chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--allow-file-access-from-files")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--enable-local-file-accesses")


chromedriver_path = ChromeDriverManager().install()
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)


temp_dir_path = os.path.abspath("Frontend/Files")
os.makedirs(temp_dir_path, exist_ok=True)

def SetAssistantStatus(status):
    status_file = os.path.join(temp_dir_path, "Status.data")
    with open(status_file, "w", encoding="utf-8") as file:
        file.write(status)

def QueryModifier(query):
    new_query = query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's", "Can you"]

    if any(word + " " in new_query for word in question_words):
        new_query = new_query.rstrip(".?!") + "?"
    else:
        new_query = new_query.rstrip(".?!") + "."

    return new_query.capitalize()

def UniversalTranslator(text):
    english_translation = mt.translate(text, "en", "auto")
    return english_translation.capitalize()

def SpeechRecognition():
    driver.get(file_url) 

    try:
       
        start_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "start"))
        )
        start_button.click() 

    except Exception as e:
        print(f"Error: Unable to find 'start' button! {e}")
        driver.quit()  
        return ""

    while True:
        try:
            
            text_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "output"))
            )
            Text = text_element.text.strip()
            
            if Text:
                driver.find_element(By.ID, "end").click()  # Stop recognition
                
                if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                    return QueryModifier(Text)
                else:
                    SetAssistantStatus("Translating...")
                    return QueryModifier(UniversalTranslator(Text))
        except Exception:
            pass

if __name__ == "__main__":
    while True:
        text = SpeechRecognition()
        print(text)
