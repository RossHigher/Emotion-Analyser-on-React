import React, { useState } from "react";
import axios from "axios";
import { Card, CardContent, Button, TextField } from "@mui/material";
import { motion } from "framer-motion";

// Определяем тип сообщения
type Message = {
  text: string;
  isUser: boolean; // Определяет, кто отправил сообщение
};

const EmotionAnalysis: React.FC = () => {
  const [inputText, setInputText] = useState<string>("");
  const [messages, setMessages] = useState<Message[]>([]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>): void => {
    setInputText(e.target.value);
  };

  const handleSendMessage = async (): Promise<void> => {
    if (inputText.trim() === "") {
      return; // Если поле ввода пустое, не отправлять ничего
    }

    // Добавляем сообщение пользователя
    const userMessage: Message = { text: inputText, isUser: true };
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    // Очищаем поле ввода
    setInputText("");

    try {
      // Добавляем задержку для имитации обработки
      await new Promise((resolve) => setTimeout(resolve, 1000));

      // Запрос к бэкенду
      const response = await axios.post<{ emotions: string[] }>(
        "http://127.0.0.1:8000/api/analyze",
        { text: userMessage.text }
      );

      const appResponse: Message = {
        text: `Emotions: ${response.data.emotions.join(", ")}`,
        isUser: false,
      };

      // Добавляем ответ приложения к переписке
      setMessages((prevMessages) => [...prevMessages, appResponse]);
    } catch (error) {
      console.error("Error analyzing text:", error);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Emotion Analysis Chat</h1>
      <div
        style={{ maxHeight: "400px", overflowY: "auto", marginBottom: "10px" }}
      >
        {messages.map((message, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }} // Анимация появления сообщения
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Card
              style={{
                alignSelf: message.isUser ? "flex-end" : "flex-start", // Сообщения пользователя справа, ответа — слева
                backgroundColor: message.isUser ? "#e1f5fe" : "#fff",
                marginBottom: "10px",
              }}
            >
              <CardContent>{message.text}</CardContent>
            </Card>
          </motion.div>
        ))}
      </div>
      <div>
        <TextField
          value={inputText}
          onChange={handleInputChange}
          placeholder="Type your message..."
          fullWidth
          style={{ backgroundColor: "white" }} // Белое поле ввода
        />
        <Button
          onClick={handleSendMessage}
          variant="contained"
          color="primary"
          style={{ marginTop: "10px" }}
        >
          Send
        </Button>
      </div>
    </div>
  );
};

export default EmotionAnalysis;

// npm run dev
