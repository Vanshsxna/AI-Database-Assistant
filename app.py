import pandas as pd
import streamlit as st

from core.database import Database
from ai.interpreter import Interpreter, UnsupportedRequestError, InterpreterError


st.set_page_config(
    page_title="Natural Language Database",
    page_icon="🗃️",
    layout="wide"
)


@st.cache_resource
def get_db():
    return Database("data/mydb.json")


@st.cache_resource
def get_interpreter():
    return Interpreter()


def get_executor(db):
    from ai.executor import Executor
    return Executor(db)


db = get_db()
interpreter = get_interpreter()
executor = get_executor(db)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hi! I'm your database assistant. Tell me what you'd like "
                "to do — e.g. *\"create a students table with id, name and "
                "marks\"* or *\"add a student with id 1, name Vansh, marks 95\"*."
            ),
            "data": None,
        }
    ]


with st.sidebar:
    st.header("Tables")

    tables = db.list_tables()

    if not tables:
        st.caption("No tables yet — try asking me to create one.")
    else:
        for table_name in tables:
            with st.expander(table_name):
                info = db.table_info(table_name)
                if info["success"]:
                    schema_rows = [
                        {
                            "column": col,
                            "type": meta["type"],
                            "pk": meta["constraints"]["primary_key"],
                            "unique": meta["constraints"]["unique"],
                            "nullable": meta["constraints"]["nullable"],
                            "default": meta["constraints"]["default"],
                        }
                        for col, meta in info["data"].items()
                    ]
                    st.dataframe(
                        pd.DataFrame(schema_rows),
                        hide_index=True,
                        use_container_width=True
                    )

                    count_result = db.count(table_name)
                    if count_result["success"]:
                        st.caption(f"{count_result['data']} row(s)")

    st.divider()

    if st.button("🧹 Clear chat", use_container_width=True):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()


st.title("Natural Language Database")
st.caption("Talk to your database.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        data = message.get("data")

        if isinstance(data, list) and data:
            st.dataframe(pd.DataFrame(data), hide_index=True, use_container_width=True)
        elif isinstance(data, dict) and data:
            st.json(data)


user_input = st.chat_input("e.g. add a student with id 1, name Vansh, marks 95")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "data": None,
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            reply_text = None
            reply_data = None

            try:
                command = interpreter.interpret(user_input)
                result = executor.execute(command)

                reply_text = result.get("message", "Done.")
                reply_data = result.get("data")

                if not result.get("success", True):
                    reply_text = f"{reply_text}"

            except UnsupportedRequestError:
                reply_text = (
                    "I couldn't match that to a database action. Try "
                    "rephrasing — e.g. \"show all students\" or "
                    "\"delete students with marks below 40\"."
                )

            except InterpreterError as e:
                reply_text = f" I had trouble understanding that: {e}"

            except ValueError as e:
                # Raised by Executor for missing/invalid required fields
                reply_text = f" {e}"

            except Exception as e:
                reply_text = f" Something went wrong: {e}"

            st.markdown(reply_text)

            if isinstance(reply_data, list) and reply_data:
                st.dataframe(pd.DataFrame(reply_data), hide_index=True, use_container_width=True)
            elif isinstance(reply_data, dict) and reply_data:
                st.json(reply_data)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply_text,
        "data": reply_data,
    })