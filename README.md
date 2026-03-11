# ⚙️ Mini Matching Engine

A simple matching engine built in Python to simulate real-world trade order matching logic. This was developed as part of a company challenge within a strict 7-day deadline.

## 🚀 Features

- Buy/Sell Order Matching
- Price-Time Priority (Reg NMS Style)
- Order Book Management
- Trade Execution Logs (In-Memory)
- CLI Interface for Testing

## 🧠 What I Learned

- Order matching logic used in stock/crypto exchanges
- Object-oriented programming for system design
- Fast prototyping under real-world time constraints
- Using AI tools like ChatGPT to debug, learn, and deliver under pressure

## 📁 Project Structure
Client
  ↓
REST API (FastAPI)
  ↓
Order Book
  ↓
Matching Engine
  ↓
Trade Execution
  ↓
WebSocket Broadcast

## 💁🏻‍♂️ Supported Order Types

Market Orders

Limit Orders

IOC (Immediate or Cancel)

FOK (Fill or Kill)
