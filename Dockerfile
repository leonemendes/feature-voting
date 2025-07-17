FROM node:18

RUN npm install -g @anthropic-ai/claude-code

WORKDIR /workspace

VOLUME ["/workspace"]

CMD [ "bash" ]