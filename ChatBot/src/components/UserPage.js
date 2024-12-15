import React, { useState } from "react";
import '../styles/userpage.css';
import ChatMessage from './ChatMessage';

function UserPage() {
    const [inputValue, setInputValue] = useState("");
    const [suggestions, setSuggestions] = useState([]);
    const [spellCorrections, setSpellCorrections] = useState([]);
    const [currentIndex, setCurrentIndex] = useState(-1);
    const [chatMessages, setChatMessages] = useState([
        { sender: "bot", text: "Hello! How can I assist you today?" }
    ]);

    const fetchSuggestions = async (prefix) => {
        if (prefix.length > 0) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/suggest?prefix=${prefix}`);
                const data = await response.json();
                setSuggestions(data);
            } catch (error) {
                console.error("Error fetching suggestions:", error);
            }
        } else {
            setSuggestions([]);
        }
    };

    const fetchSpellCorrections = async (word) => {
        if (word.length > 0) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/spellcorrect?word=${word}`);
                const data = await response.json();
                setSpellCorrections(data);
            } catch (error) {
                console.error("Error fetching spell corrections:", error);
            }
        } else {
            setSpellCorrections([]);
        }
    };

    const handleInputChange = (event) => {
        const value = event.target.value;
        setInputValue(value);

        const lastWord = value.split(" ").pop();
        fetchSuggestions(lastWord);
        fetchSpellCorrections(lastWord); 
        setCurrentIndex(-1); 
    };

    const handleSuggestionClick = (suggestion) => {
        const words = inputValue.split(" ");
        words.pop(); 
        words.push(suggestion); 
        setInputValue(words.join(" ")); 
        setSuggestions([]);
        setSpellCorrections([]); 
    };

    const handleKeyDown = (event) => {
        if (suggestions.length === 0) return;

        if (event.key === "ArrowDown") {
            setCurrentIndex((prevIndex) => Math.min(prevIndex + 1, suggestions.length - 1));
        } else if (event.key === "ArrowUp") {
            setCurrentIndex((prevIndex) => Math.max(prevIndex - 1, 0));
        } else if (event.key === "Enter" && currentIndex >= 0) {
            handleSuggestionClick(suggestions[currentIndex]);
            event.preventDefault();
        }
    };

    const sendUserInput = async (inputValue) => {
        if (inputValue.length > 3) {
            setChatMessages((prevMessages) => [...prevMessages, { sender: "user", text: inputValue }]);
            
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/chat`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ message: inputValue })
                });
    
                if (response.ok) {
                    const data = await response.json();

                    setChatMessages((prevMessages) => [...prevMessages, { sender: "bot", text: data.response }]);
                } else {
                    console.error("Error:", response.statusText);
                }
            } catch (error) {
                console.error("Error sending user input:", error);
            }
        }
    };

    const handleSend = () => {
        if (inputValue.trim() !== "") {
            sendUserInput(inputValue);
            setInputValue("");
        }
    };

    return (
        <div className="UserPage">
            <div className="chat-container">
                <div className="chat-header"><h2>TechHelp</h2></div>
                <div className="chat-messages" id="chatMessages">
                    {chatMessages.map((message, index) => (
                        <ChatMessage key={index} sender={message.sender} text={message.text} />
                    ))}
                </div>
                <div className="chat-input">
                    <input
                        type="text"
                        id="userInput"
                        placeholder="Type your message here..."
                        value={inputValue}
                        onChange={handleInputChange}
                        onKeyDown={handleKeyDown}
                    />
                    <div className="suggestions-container">
                        {suggestions.slice(0, 5).map((suggestion, index) => (
                            <div
                                key={index}
                                className={`suggestion-item ${index === currentIndex ? "highlighted" : ""}`}
                                onClick={() => handleSuggestionClick(suggestion)}
                                onMouseEnter={() => setCurrentIndex(index)}
                            >
                                {suggestion}
                            </div>
                        ))}
                    </div>
                    <div className="spell-corrections-container">
                        <h4>Did you mean:</h4>
                        {spellCorrections.map((correction, index) => (
                            <div
                                key={index}
                                className="correction-item"
                                onClick={() => handleSuggestionClick(correction)}
                            >
                                {correction}
                            </div>
                        ))}
                    </div>
                    <button onClick={handleSend}>Send</button>
                </div>
            </div>
        </div>
    );
}

export default UserPage;