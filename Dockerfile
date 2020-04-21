FROM python:3.7

EXPOSE 8501

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .
RUN mkdir -p /root/.streamlit

RUN bash -c 'echo -e "\
	[server]\n\
	enableCORS = false\n\
	" > /root/.streamlit/config.toml'

EXPOSE 8501
EXPOSE 8080

# --------------- Export envirennement variable ---------------
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

CMD ["streamlit", "run", "--server.port", "8080", "main.py"]