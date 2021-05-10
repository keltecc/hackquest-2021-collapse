#!/bin/bash

dotnet publish \
    -o ./deploy/service/ \
    -c Release \
    /p:DebugType=None \
    /p:DebugSymbols=false \
    -p:Configuration=Release \
    src/ZN.Runner
