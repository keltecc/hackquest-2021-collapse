FROM mcr.microsoft.com/dotnet/runtime:3.1

RUN apt update \
    && apt install -y socat libgomp1

RUN useradd -M -s /bin/false collapse

WORKDIR /var/collapse/

COPY ./service/ flag.txt /var/collapse/

USER collapse

ENTRYPOINT socat TCP-LISTEN:31337,reuseaddr,fork EXEC:"./ZN.Runner"
