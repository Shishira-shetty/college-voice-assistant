import speech_recognition as sr
import pyttsx3
import time
import queue
import threading
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import random  # Import the random library

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

    def process_command(self, command):
        """Process the user's voice command and return a response."""
        command = command.lower()
        if "hello" in command:
            return "Hi there! Welcome to RNS First Grade College Autonomous! How can I assist you today?"
        elif "time" in command:
            return f"The current time is {time.strftime('%H:%M:%S')}."
        elif "courses" in command or "subjects" in command:
            return ("RNS FGCA offers undergraduate programs including Bachelor of Computer Applications (BCA), Bachelor of Commerce (BCom), "
                    "Bachelor of Business Administration (BBA), and a Master of Business Administration (MBA) started in 2023. These programs "
                    "focus on technical and management education with industry-relevant curricula.")
        elif "bca" in command or "bachelor of computer application" in command:
            return ("The BCA program at RNS FGCA provides a flexible curriculum aligned with the latest IT trends. It includes hands-on learning "
                    "through projects, internships, and IT clubs like 'Cront,' preparing students for careers in software development, data science, "
                    "and more.")
        elif "bcom" in command or "bachelor of commerce" in command:
            return ("The BCom program focuses on accounting, finance, management, and banking. It emphasizes skill-based activities and experiential "
                    "learning to prepare students for careers in civil services, finance, and entrepreneurship.")
        elif "bba" in command or "bachelor of business administration" in command:
            return ("The BBA program includes specializations like Marketing and Human Resource Management. It offers add-on courses such as Digital "
                    "Marketing and Tally with GST, aiming to develop leadership and critical thinking skills for business careers.")
        elif "mba" in command or "master of business administration" in command:
            return ("Started in 2023, the MBA program at RNS FGCA empowers aspiring leaders with skills for the evolving business world, featuring "
                    "real-world applications and a focus on personal growth.")
        elif "schedule" in command or "timetable" in command:
            return ("The college operates from 8:30 AM to 4 PM, Monday to Saturday. Specific schedules vary by course—check with the administration "
                    "for your program’s timetable!")
        elif "faculty" in command or "teachers" in command:
            return ("RNS FGCA boasts highly knowledgeable faculty across departments, dedicated to experiential learning and student mentorship. "
                    "Contact +91-123-456-7890 or principal_rnsfgc@rnsgi.com for specific department details.")
        elif "exam" in command or "test" in command:
            return ("Exams occur at semester-end with midterms in between. Dates are posted on the college notice board or website, rnsfgc.edu.in.")
        elif "library" in command:
            return ("The library, established in 2012, is open from 8 AM to 5 PM with an open-access system, automated with Koha software. It offers "
                    "books, journals, e-resources, and OPAC for searching.")
        elif "contact" in command or "phone" in command:
            return ("Reach RNS FGCA at Dr. Vishnuvardhan Road, Channasandra, RR Nagar Post, Bengaluru, Karnataka – 560098. Phone: +91-123-456-7890, "
                    "Email: principal_rnsfgc@rnsgi.com.")
        elif "location" in command or "where" in command:
            return ("RNS FGCA is located at Dr. Vishnuvardhan Road, Channasandra, RR Nagar, Bangalore, Karnataka – 560098. It’s a serene campus with "
                    "lush greenery and elegant architecture.")
        elif "founder" in command or "dr. r. n. shetty" in command:
            return ("Dr. R. N. Shetty, born on August 15, 1928, is the founder of RNS FGCA. A visionary industrialist and philanthropist, he’s known "
                    "for iconic constructions and contributions to Karnataka’s development, earning awards like the Rajyotsava Award.")
        elif "facilities" in command or "campus" in command:
            return ("The campus features cutting-edge labs, a vibrant library, sports facilities, and a business lab for hands-on learning. It’s "
                    "designed with lush greenery and elegant architecture for an inspiring environment.")
        elif "about" in command or "college" in command or "rns fgca" in command:
            return ("RNS First Grade College, established in 2012 in Bangalore, Karnataka, is a premier institution founded by Dr. R. N. Shetty, "
                    "a renowned industrialist and philanthropist. It holds an 'A' Grade from NAAC and achieved autonomous status in 2024, "
                    "offering enhanced educational flexibility. The college is affiliated with Bangalore University and is known for its "
                    "experiential learning, lush green campus, and commitment to fostering leaders in a global landscape.")
        else:
            return "I’m not sure how to answer that. Try asking about courses, faculty, facilities, or the college’s history!"

class GuiVoiceAssistant(VoiceAssistant):
    def __init__(self, message_queue):
        super().__init__()
        self.message_queue = message_queue
        self.stop_flag = False

    def listen(self):
        """Listen for voice input and return transcribed text."""
        with self.microphone as source:
            self.message_queue.put("Adjusting for ambient noise... Please wait")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            self.message_queue.put("Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                text = self.recognizer.recognize_google(audio)
                self.message_queue.put(f"You said: {text}")
                return text.lower()
            except sr.WaitTimeoutError:
                self.message_queue.put("No speech detected within 5 seconds")
                return None
            except sr.UnknownValueError:
                self.message_queue.put("Sorry, I couldn’t understand that")
                return None
            except sr.RequestError as e:
                self.message_queue.put(f"Could not request results; {e}")
                return None

    def speak(self, text):
        """Convert text to speech and update the queue."""
        self.message_queue.put("Speaking...")
        self.message_queue.put(f"Replying: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            self.message_queue.put("Finished speaking")
        except Exception as e:
            self.message_queue.put(f"Error while speaking: {e}")

    def run(self):
        """Main loop for the voice assistant."""
        self.speak("Welcome to RNS FGCA! I’m your assistant for all college-related queries.")
        while not self.stop_flag:
            command = self.listen()
            if command:
                if "bye" in command or "exit" in command:
                    self.speak("Goodbye! Have a great day at RNS FGCA!")
                    self.stop_flag = True
                    break
                response = self.process_command(command)
                self.speak(response)
            time.sleep(0.5)

    def stop(self):
        """Stop the assistant."""
        self.stop_flag = True

def update_gui(root, text_widget, message_queue):
    """Update the GUI with messages from the queue."""
    while True:
        try:
            message = message_queue.get_nowait()
            text_widget.insert(tk.END, message + "\n")
            text_widget.see(tk.END)
        except queue.Empty:
            break
    root.after(100, update_gui, root, text_widget, message_queue)

def change_background(root, background_label, image_paths):
    """Change the background image randomly every 3 seconds."""
    image_path = random.choice(image_paths)  # Randomly select an image
    try:
        bg_image = Image.open(image_path)
        bg_image = bg_image.resize((1400, 1500), Image.Resampling.LANCZOS)  # Resize to fit window
        bg_photo = ImageTk.PhotoImage(bg_image)
        background_label.config(image=bg_photo)
        background_label.image = bg_photo  # Keep a reference to avoid garbage collection
    except FileNotFoundError:
        print(f"Image not found: {image_path}")
    root.after(5000, change_background, root, background_label, image_paths)  # Repeat every 3 seconds

if __name__ == "__main__":
    # Initialize the message queue and assistant
    message_queue = queue.Queue()
    assistant = GuiVoiceAssistant(message_queue)

    # Set up the GUI
    root = tk.Tk()
    root.title("RNS FGCA Voice Assistant")
    root.geometry("1400x1500")

    # List of image paths for the background
    image_paths = [
        "image1.jpg",  # Replace with your image paths
        "image2.jpg",
        "image3.jpg",
        "image4.jpg",
        "image5.jpg"
    ]

    # Add a background label (initially empty)
    background_label = tk.Label(root)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover entire window

    # Start the background image changer
    change_background(root, background_label, image_paths)

    # Add a scrolled text widget to display messages (on top of background)
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=10, height=15, bg="white", fg="black")
    text_area.pack(padx=200, pady=200, fill=tk.BOTH, expand=False)

    # Add a stop button
    stop_button = tk.Button(root, text="Stop", command=assistant.stop, bg="red", fg="white", font=("calibri", 18, "bold"), width=5, height=2)
    stop_button.pack(pady=50)

    # Start the assistant in a separate thread
    assistant_thread = threading.Thread(target=assistant.run)
    assistant_thread.daemon = True
    assistant_thread.start()

    # Start the GUI update loop
    root.after(100, update_gui, root, text_area, message_queue)

    # Run the Tkinter main loop
    root.mainloop()

    # Ensure the assistant stops when the window is closed
    assistant.stop()
    assistant_thread.join(timeout=1.0)
