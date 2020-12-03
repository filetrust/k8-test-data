FROM centos:7
RUN yum -y install epel-release; \
    yum -y install python-pip; yum clean all;

RUN yum install libfreetype.so.6 -y yum install libpthread.so.0 -y yum install fontconfig -y 



RUN yum install git -y
RUN yum groupinstall "Development Tools" -y
WORKDIR /
RUN git clone https://github.com/wolfcw/libfaketime.git
WORKDIR /libfaketime/src
RUN make install


COPY ["CLI/glasswallCLI"           , "/usr/bin"        ] 
COPY ["Library/libglasswall.classic.so", "/usr/lib"        ]
COPY ["CLI/Configs/*"              , "/home/glasswall/"]
RUN ln -s /usr/lib/libglasswall.classic.so /usr/bin/libglasswall.classic.so
RUN ldconfig
RUN chmod +x /usr/bin/glasswallCLI

COPY requirements.txt .
RUN pip install -r requirements.txt



SHELL [ "/bin/bash", "-c" ]
ENV LD_PRELOAD=/usr/local/lib/faketime/libfaketime.so.1
ENV FAKETIME_NO_CACHE=1
ENV FAKETIME=2020-10-29\ 12:00:00



WORKDIR /usr/src/app
COPY . .
CMD [ "python", "main.py" ]
