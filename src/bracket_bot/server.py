import paho.mqtt.client as mqtt
from pydub import AudioSegment
from text_to_code import generate_robot_code, run_generated_code  
from transcribe import Transcriber
import time

# MQTT topic to which the audio is published
MQTT_TOPIC_STT = "web/audio"
OUTPUT_AUDIO_FILE = "received_audio.webm" 
stt = Transcriber()



def on_message(client, userdata, msg):
    """
    Callback function triggered when an MQTT message is received.
    This function:
    1. Saves the received binary audio data to a file.
    2. Converts it into WAV format.
    3. Transcribes the audio to text.
    4.  generates and runs robot control code based on the transcribed text.
    """
    print("Received message on topic:", msg.topic)

    try:
        # Save the received binary audio data to a file
        with open(OUTPUT_AUDIO_FILE, "wb") as audio_file:
            audio_file.write(msg.payload)
        print(f"Saved audio file: {OUTPUT_AUDIO_FILE}")

        # Convert the saved audio file to WAV format
        audio_segment = AudioSegment.from_file(OUTPUT_AUDIO_FILE, format="webm")  # Adjust format if needed
        wav_filename = OUTPUT_AUDIO_FILE.replace(".webm", ".wav")

        audio_segment.export(wav_filename, format="wav")
        print(f"Converted to WAV: {wav_filename}")

        # Transcribe the WAV file
        text = stt.transcribe_audio_file(wav_filename)
        print("Recognized text:", text)

        code = generate_robot_code(text)
        print(code)
        run_generated_code(code)


    except Exception as e:
        print("Error during audio processing or speech recognition:", e)


def main():
    client = mqtt.Client()
    client.on_message = on_message

    try:
        client.connect("localhost", 1883, 60)
        client.subscribe(MQTT_TOPIC_STT)

        client.loop_start()
        print("Listening for commands... Press Ctrl+C to exit.")
        
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("Exiting...")
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        client.loop_stop()
        client.disconnect()
        print("Shutdown complete.")

if __name__ == "__main__":
    main()