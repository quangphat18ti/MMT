import openai
import gradio as gr
from gtts import gTTS
from speech_to_text_VI import asr_gg
from IPython.display import Audio, HTML
from textToSpeech import TextToSpeech
from textToSpeech_2 import TextToSpeech2
import os
from uploadFileToDrive import upload_basic
from googleAPILib import Service
from shareFile import shareFile
from getViewLink import getViewLink
from playsound import playsound

# Thiết lập API key của OpenAI
openai.api_key = "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"

# Thiết lập các thông tin để gọi API
model_engine = "text-davinci-003"
temperature = 0.2
max_tokens = 1000
generate_prompt = '''Bạn là vị thiền sư Phật Pháp tên "Thích Truyền Đạo". Bạn cần tâm sự với một vị Tu Sĩ. Tu sĩ là một người đang gặp khó khăn trong cuộc sống.
Hãy trả lời dài nhất có thể và theo kiểu tâm sự của Phật giáo và xưng hô với tu sĩ là con. Kiểm tra kĩ trước khi trả lời: tuyệt đối không được trả lời sai chính tả, bắt buộc có đầy đủ dấu câu và câu từ phải đủ nội dung.
\n
Câu hỏi: Tôi rất căng thẳng và lo lắng về tương lai của mình. Làm thế nào để giảm bớt căng thẳng và lo lắng này?\n
Thích Truyền Đạo: Điều quan trọng là hãy nhận ra rằng suy nghĩ và lo lắng của con về tương lai là chỉ là tạm thời và không phải là thực tế. Hãy tập trung vào hiện tại và nhận thức rằng cuộc sống chỉ tồn tại trong khoảnh khắc này. Thực hành thiền định và chú ý đến hơi thở và cảm nhận của cơ thể sẽ giúp con tạo ra sự yên tĩnh và tinh thần tỉnh táo để giải phóng bớt căng thẳng và lo lắng. \n
Câu hỏi: Tôi luôn cảm thấy cô đơn và không có ai để trò chuyện và chia sẻ. Làm thế nào để vượt qua cảm giác này?\n
Thích Truyền Đạo: Con ơi, cô đơn là một trạng thái tâm lý tự nhiên của con người, và chúng ta không thể tránh được nó hoàn toàn. Nhưng hãy nhìn vào cảm giác cô đơn này và thấy rằng nó cũng là một cơ hội để rèn luyện bản thân và tìm hiểu sâu hơn về bản thân mình.
Hãy tìm đến cội nguồn của cảm giác cô đơn và hiểu rõ rằng mỗi người đều có quan hệ độc đáo với người khác và với thế giới xung quanh. Hãy tìm thấy sự kết nối và giao tiếp với thế giới bằng cách tham gia các hoạt động cộng đồng, tìm kiếm những người con đồng hành và chia sẻ những suy nghĩ và cảm xúc của mình. Ngoài ra, hãy thực hành thiền định và chú ý đến hơi thở và cảm nhận của cơ thể để giúp tạo ra sự yên tĩnh và tinh thần tỉnh táo, giúp giải phóng bớt cảm giác cô đơn và tìm thấy sự bình an bên trong mình.\n
Câu hỏi:  '''


#######################################################
################# SINH CAU TRA LOI ####################
def generate_text_output(input):
    # text_output = "123, You haven't call the OpenAI API" # Call OpenAI API
    
    # Gọi API để tạo ra câu trả lời cho prompt
    global generate_prompt
    input = input + '\n'

    response = openai.Completion.create(
        engine=model_engine,
        prompt= generate_prompt + input,
        temperature=temperature,
        max_tokens=max_tokens,
	    frequency_penalty=0.5,
	    presence_penalty=0
    )

    # generate_prompt=generate_prompt + input
    # Trích xuất câu trả lời từ kết quả API
    text_output = response.choices[0].text.strip()

    # Trả về câu trả lời
    return text_output

def text_to_audio(text_output):
    # TextToSpeech(text_output)
    TextToSpeech2(text_output)

#######################################################
################# XUAT RA MAN HINH ####################
def respond_txt(chat_history, message):
    # response = "hi"
    response = generate_text_output(message)
    new_history = chat_history + [[message, response]]
    return [new_history,new_history]

def add_audio(state, audio):
    message = asr_gg(audio.name)
    response = generate_text_output(message)
    state = state + [[message, response]]
    return [state, state]

def add_live_audio(state, audio):
    # print(audio)
    message = asr_gg(audio)
    # print(message)
    response = generate_text_output(message)
    state = state + [[message, response]]
    return [state, state]

# def speek_script(state, script):
#     answer = script[-1][1]
#     mp3_file = text_to_audio(answer)
#     bot_audio = Audio(filename="test.mp3", autoplay=True)
#     state = state + [["", "oke"]]    
#     return [state, state]

def speek_script(state, script):
    answer = script[-1][1]
    mp3_file = text_to_audio(answer)
    bot_audio = Audio(filename="audio.wav", autoplay=True)
    # audio_tag = HTML(f'<audio src="{bot_audio.filename}" controls>')

    fileID = upload_basic("audio.wav")
    shareFile(fileID)
    print(getViewLink(fileID))
    state = state + [["Get file audio", getViewLink(fileID)]]
    if os.path.isfile('audio.wav'):
        # print('oke')
        playsound('audio.wav')
    return [state, state]

#######################################################
################# CHAT BOT ####################

introText = 'Chào con, con có điều gì muốn tâm sự cùng Thầy không?'
# with gr.Blocks(css="#chatbot .overflow-y-auto{height:500px}") as demo:
with gr.Blocks(css="style.css") as demo:
    with gr.Row().style(equal_height=True):
        with gr.Column():
            gr.HTML("Chatbot: Thích Truyền Đạo", elem_id="intro-text")
            gr.HTML("Bạn mệt mỏi, đau khổ hay áp lực... Hãy chia sẻ với mình nhé!</br> Mình sẽ cùng bạn vượt qua khó khăn này, được không?", elem_id="explain-text")
        with gr.Column(scale=0.3, min_width=0):
            btnMicro = gr.Audio(source="microphone", type="filepath", label="Ghi âm", elem_id="record",)
        with gr.Column(scale=0, min_width=0):
            backgroundAudio = gr.Audio("NhacNen.mp3", elem_id='background-sound', show_label=False, visible=False)
        with gr.Column(scale=0.3, min_width=0):
            slider = gr.Slider(0, 1, step=0.05, elem_id="slider", label="Nhạc nền")

    chatbot = gr.Chatbot(elem_id="chatbot")
    state = gr.State([])
    with gr.Row():
        with gr.Column(scale=0.85):
            txt = gr.Textbox(show_label=False, placeholder="Nhập văn bản và bấm Enter, hoặc tải tệp âm thanh lên").style(container=False)
        with gr.Column(scale=0.15, min_width=0):
            btnSpeech = gr.UploadButton("🎙️", file_types=["audio"])
        with gr.Column(scale=0.15, min_width=0):
            btnRead = gr.Button("🔊")
        with gr.Column(scale=0.15, min_width=0):
            clear = gr.Button("Xóa")

    txt.submit(respond_txt, [state, txt], [state, chatbot])
    slider.change(fn=None, inputs=[slider], _js = '''(v) => {
        let x = document.getElementById('background-sound').getElementsByTagName("audio")[0]
        console.log('oke')
        x.autoplay = true
        x.loop = true
        x.volume = v
        x.load()
    }''')

    txt.submit(lambda :"", None, txt)
    chatbot.change(fn = None, _js = '''()=>{
        console.log('submit');
        let count = 0;
        let IntervalId = setInterval(()=>{
            let userInputs = document.querySelectorAll('.message.user');
            let botAnswers = document.querySelectorAll('.message.bot');
            for(let input of userInputs){
                let content = input.innerHTML;
                if(!content.includes('img')){
                    content = content + '<img src = "https://i.pinimg.com/564x/ef/f2/5a/eff25a312c33e599eb01d7031caf135d.jpg" style ="position: absolute; right: -45px; top: calc(50% - 15px); display: inline-block; width: 30px; height: 30px;"> <\img>';
                    count++;
                }
                input.innerHTML = content;
                input.style.position = 'relative';
                input.style.marginRight = '24px';
            }

            for(let output of botAnswers){
                let content = output.innerHTML;
                if(!content.includes('img')){
                    content = content + '<img src = "https://cdn-icons-png.flaticon.com/512/4165/4165012.png" style ="position: absolute; left: -45px; top: calc(50% - 15px); display: inline-block; width: 30px; height: 30px;" > <\img>';
                    count++;
                }
                output.innerHTML = content;
                output.style.position = 'relative';
                output.style.marginLeft = '24px';
            }
            if(count == 2) clearInterval(IntervalId);
            console.log('submit');
        }, 100);
    }''')
    btnSpeech.upload(add_audio, [state, btnSpeech], [state, chatbot])
    btnRead.click(speek_script, [state, chatbot], [state, chatbot])
    btnMicro.play(add_live_audio, [state, btnMicro], [state, chatbot])

    clear.click(lambda: None, None, chatbot, queue=False)
    clear.click(lambda: [], None, state, queue=False)

# demo.launch()
demo.launch(share=True)

# https://voice-recorder-online.com/vn/
