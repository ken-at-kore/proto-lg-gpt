# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import openai
from Contants import SYSTEM_PROMPT

LOGGER = get_logger(__name__)


def run():
  st.set_page_config(
      page_title="LG-GPT Prototype",
      page_icon="🤖",
  )

  st.title("LG-GPT Prototype")

  openai.api_key = st.secrets["OPENAI_API_KEY"]

  if "openai_model" not in st.session_state:
      st.session_state["openai_model"] = "gpt-4"

  if "messages" not in st.session_state:
      st.session_state.messages = [
          {"role": "system", "content": SYSTEM_PROMPT},
          {"role": "assistant", "content": "How can I help you?"}
        ]

  for message in st.session_state.messages:
      if message["role"] == "user" or message["role"] == "assistant":
        with st.chat_message(message["role"]):
              st.markdown(message["content"])

  if prompt := st.chat_input("What's up?"):
      st.session_state.messages.append({"role": "user", "content": prompt})
      with st.chat_message("user"):
          st.markdown(prompt)

      with st.chat_message("assistant"):
          message_placeholder = st.empty()
          full_response = ""
          for response in openai.ChatCompletion.create(
              model=st.session_state["openai_model"],
              messages=[
                  {"role": m["role"], "content": m["content"]}
                  for m in st.session_state.messages
              ],
              stream=True,
          ):
              full_response += response.choices[0].delta.get("content", "")
              message_placeholder.markdown(full_response + "▌")
          message_placeholder.markdown(full_response)
      st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    run()
