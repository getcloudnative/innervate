FROM python:2.7

ENV HOME=/opt/app-root/

RUN mkdir -p ${HOME} && \
    useradd -u 1001 -r -g 0 -d ${HOME} -s /sbin/nologin \
            -c "Default Application User" default
WORKDIR ${HOME}

COPY help.1 /
COPY config/ ${HOME}/config/
COPY innervate/ ${HOME}/innervate/
COPY setup.py ${HOME}
COPY requirements.txt ${HOME}

RUN pip install -r requirements.txt -e .

RUN chown -R 1001:0 /opt/app-root && \
    find ${HOME} -type d -exec chmod g+ws {} \;

USER 1001

CMD innv
