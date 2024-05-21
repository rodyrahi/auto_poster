import os
import bs4 
from html2image import Html2Image
import streamlit as st
from openai import OpenAI




openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)


if 'content' not in  st.session_state: 
    st.session_state['content'] = 'Write your content here or generate by AI'
if 'aicontent' not in  st.session_state: 
    st.session_state.aicontent = []

inputs = []

def generate_content(text_length=100, prompt="" , id=""):
    response  = client.chat.completions.create(
        model="gpt-3.5-turbo",
          messages=[
    {"role": "system", "content": "you are a content writer who creats consise and catchy lines for posters and ads."},
    {"role": "user", "content": f"{prompt} write near {text_length} "},
  ]
    )
    print(response)
    out = str(response.choices[0].message.content).strip('"')
    st.session_state.aicontent.append({"id":id,"content":out})
    return out



os.chdir(os.path.dirname(__file__))


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

    Template = st.selectbox('Select Template', ['./poster2.html', './poster.html'])
    with open(Template) as inf:
        txt = inf.read()
        soup = bs4.BeautifulSoup(txt)
  

    all_h1 = [{"id": h1.get('id'), "string": h1.get_text()} for h1 in soup.find_all('h1')]

    for i in all_h1:
        if i['id'] is not None:
            input = st.text_input(label=i['id'], value=i['string'], key=i['id'])
            inputs.append( {"id":i['id'] , "value":input} )

    
    # comp_name = st.text_input('Enter Company Name', value='Company Name')
    
    promt_col , length_col = st.columns(2) 


    with promt_col:
        selected_input = st.selectbox(label='Select Input', options=[i['id'] for i in inputs], index=0)

        prompt = st.text_input('Enter Prompt', placeholder='write prompt here')

    with length_col:
        text_length = st.number_input(label='Text Length' ,value=100, step=1 , min_value=0, max_value=500)
    
# with gen_gpt_col:
    gen_gpt_btn = st.button('🎉 Generate with AI')

    if gen_gpt_btn:
        generate_content(prompt=prompt , text_length=text_length , id=selected_input)
        # st.write(content)
    print(selected_input )

    for k in inputs:
        if k['id'] == selected_input:
            for x in st.session_state.aicontent:
                if x['id'] == selected_input:
                    k['value'] = x['content']
                    break

    
    # content = st.text_area('Enter Content', value=st.session_state['content'])

    footer = st.text_input('Enter Footer', value='Footer')
    bg_color = st.color_picker('Enter Background Color')
    image_upload = st.file_uploader('Upload Image', type=['png','jpg','jpeg'], accept_multiple_files=False)
    user_image_url = None
    if image_upload is not None:
        user_image_url = 'tmp_user_image.png'
        image_upload.seek(0)
        with open(user_image_url, 'wb') as outf:
            outf.write(image_upload.read())


# content = content.upper()


def make_header(resolution, html_path):
    
    with open(html_path) as inf:
        txt = inf.read()
        soup = bs4.BeautifulSoup(txt)

    st.write(inputs)
    st.write(all_h1)
    st.write(st.session_state.aicontent)

    for j in inputs:
        soup.find(id=j['id']).string = j['value']

        print(soup.find(id=j['id']))


        

    # soup.find(id='comp_name').string = comp_name
    # soup.find(id='main-heading').string = content
    # soup.find(id='footer-content').string = footer
    soup.find('body').attrs['style'] = f'background-color: {bg_color}; height: {resolution[1]}; width: {resolution[0]};'
    # soup.find(id='main-content').attrs['style'] = f'height: {resolution[1]};'

    
    if user_image_url is not None:
        soup.find(id='comp_img').attrs['src'] =  os.path.join(os.getcwd(), user_image_url) 


    title_html = soup.prettify()
    hti = Html2Image()
    hti.screenshot(html_str=title_html,save_as='tmp_imp.png', size=resolution)



   
with col1:
        h1c, h2c = st.columns([1,1])
        with h1c:
            width = st.number_input('width', value=1080)
        with h2c:
            height = st.number_input('height', value=1350)

        st.download_button(label='Download', data=open('tmp_imp.png', 'rb').read(), file_name='poster.png', mime='image/png')
        

    
make_header(resolution=(width, height), html_path=Template)
with col2:
    st.image('tmp_imp.png' )