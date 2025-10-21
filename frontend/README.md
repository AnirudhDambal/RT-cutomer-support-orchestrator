# Frontend - Customer Support Chat Interface

A modern, responsive React chat interface for the AI Customer Support system.

## Features

- 💬 Real-time chat interface
- 🎨 Beautiful gradient design with smooth animations
- 📱 Fully responsive (mobile, tablet, desktop)
- 🔄 Session management and chat history
- ⚡ Quick question shortcuts
- 🎯 Clear visual feedback for messages
- ⚠️ Escalation indicators
- ✨ Typing indicators

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### 3. Build for Production

```bash
npm run build
npm run preview
```

## Configuration

### API Endpoint

The frontend connects to the backend API. Edit `src/App.jsx` if you need to change the API URL:

```javascript
const API_BASE_URL = 'http://localhost:8000'
```

### Proxy Setup

The Vite config includes a proxy to avoid CORS issues during development:

```javascript
// vite.config.js
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
  }
}
```

## Features Guide

### Chat Interface

- Type messages in the input field at the bottom
- Press Enter or click the send button to send
- Messages appear in real-time with timestamps
- User messages on the right (purple), AI responses on the left (white)

### Quick Questions

Use the sidebar to quickly ask common questions:
- "What is your return policy?"
- "How can I track my order?"
- "What shipping options do you offer?"
- "Product information"

### Session Management

- Each chat creates a unique session
- Click the refresh button to start a new conversation
- Session history is maintained on the backend

### Escalation Handling

When a query needs human support:
- Yellow badge appears on the message
- Clear indication that a human agent will assist

## Customization

### Colors and Styling

Edit `src/App.css` to customize the appearance:

```css
/* Primary gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Change to your brand colors */
background: linear-gradient(135deg, #your-color-1 0%, #your-color-2 100%);
```

### Quick Questions

Add or modify quick questions in `src/App.jsx`:

```javascript
<button 
  className="quick-question"
  onClick={() => setInput("Your custom question?")}
>
  Your custom question?
</button>
```

### Contact Information

Update the contact info in the sidebar:

```javascript
<p className="contact-info">
  📧 support@company.com<br />
  📞 1-800-SUPPORT<br />
  🕐 Mon-Fri 9AM-8PM EST
</p>
```

## Component Structure

```
frontend/
├── index.html          # HTML template
├── package.json        # Dependencies
├── vite.config.js      # Vite configuration
└── src/
    ├── main.jsx        # App entry point
    ├── App.jsx         # Main chat component
    ├── App.css         # Styles
    └── index.css       # Global styles
```

## Technologies Used

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Axios** - HTTP client for API calls
- **CSS3** - Styling with gradients and animations

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Performance

The app is optimized for:
- Fast initial load
- Smooth scrolling
- Efficient re-renders
- Minimal bundle size

## Troubleshooting

**Issue: Cannot connect to backend**
- Ensure the backend is running on `http://localhost:8000`
- Check CORS settings in the backend
- Verify the API_BASE_URL in App.jsx

**Issue: Messages not scrolling**
- This is handled automatically with useRef
- Check browser console for errors

**Issue: Styling issues**
- Clear browser cache
- Run `npm run build` to rebuild
- Check for CSS conflicts

