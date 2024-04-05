import os
import bs4 
from html2image import Html2Image
import streamlit as st
# from openai import OpenAI






openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)



if 'content' not in  st.session_state: 
    st.session_state['content'] = 'Write your content here or generate by AI'

def generate_content(text_length=100, prompt=""):
    response  = client.chat.completions.create(
        model="gpt-3.5-turbo",
          messages=[
    {"role": "system", "content": "you are a content writer who creats consise and catchy lines for posters and ads."},
    {"role": "user", "content": f"{prompt} write near {text_length} "},
  ]
    )
    print(response)
    out = str(response.choices[0].message.content).strip('"')
    st.session_state['content'] = out
    return out



os.chdir(os.path.dirname(__file__))
# set st backgound color

st.set_page_config(layout="wide") 
st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
                
        </style>
        """, unsafe_allow_html=True)


st.title = 'Poster Creator'
st.header('Auto Poster Creator')

col1, mid_m, col2 = st.columns([3,0.5 ,2])

with col1:
    content = None
    comp_name = st.text_input('Enter Company Name', value='Company Name')
    
    promt_col , length_col = st.columns(2) 

    with promt_col:
        prompt = st.text_input('Enter Prompt', placeholder='write prompt here')

    with length_col:
        text_length = st.number_input(label='Text Length' ,value=100, step=1 , min_value=0, max_value=500)
# with gen_gpt_col:
    gen_gpt_btn = st.button('🎉 Generate with AI')

    if gen_gpt_btn:
        generate_content(prompt=prompt , text_length=text_length)
        # st.write(content)
    
    content = st.text_area('Enter Content', value=st.session_state['content'])

    footer = st.text_input('Enter Footer', value='Footer')
    bg_color = st.color_picker('Enter Background Color')
    image_upload = st.file_uploader('Upload Image', type=['png','jpg','jpeg'], accept_multiple_files=False)
    user_image_url = None
    if image_upload is not None:
        user_image_url = 'tmp_user_image.png'
        image_upload.seek(0)
        with open(user_image_url, 'wb') as outf:
            outf.write(image_upload.read())


content = content.upper()


def make_header(resolution, html_path):
    
    with open(html_path) as inf:
        txt = inf.read()
        soup = bs4.BeautifulSoup(txt)



    soup.find(id='comp_name').string = comp_name
    soup.find(id='main-heading').string = content
    soup.find(id='footer-content').string = footer
    soup.find(id='bg-color').attrs['style'] = f'background-color: {bg_color}; height: {resolution[1]}; width: {resolution[0]};'
    soup.find(id='main-content').attrs['style'] = f'height: {resolution[1]};'

    
    if user_image_url is not None:
        soup.find(id='comp_img').attrs['src'] =  os.path.join(os.getcwd(), user_image_url) #  user_image_url
    title_html = soup.prettify()
    hti = Html2Image()
    hti.screenshot(html_str=title_html,save_as='tmp_imp.png', size=resolution)


width = 1080
height = 1350
make_header(resolution=(width, height), html_path=r'D:\auto_poster\poster.html')

with col2:
    st.image('tmp_imp.png' )
   
with col1:
        h1c, h2c = st.columns([1,1])
        with h1c:
            width = st.number_input('width', value=1080)
        with h2c:
            height = st.number_input('height', value=1350)

        st.download_button(label='Download', data=open('tmp_imp.png', 'rb').read(), file_name='poster.png', mime='image/png')
        # st.success('Your Poster is Downloaded Successfully!')

    
