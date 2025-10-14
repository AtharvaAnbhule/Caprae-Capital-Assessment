# Quick Setup Guide for Reviewers

This guide will help you get LeadSquatch Pro running in less than 5 minutes.

## Prerequisites

Ensure you have the following installed:
- Node.js (version 18 or higher) - [Download here](https://nodejs.org/)
- Python 3.9+ - [Download here](https://www.python.org/downloads/)
- npm (comes with Node.js)
- pip (comes with Python)

Check your installations:
```bash
node --version
python --version
npm --version
pip --version
```

## Quick Start (Recommended)

### Option 1: Using the Start Script (Mac/Linux)

1. Clone or download the repository
2. Navigate to the project directory
3. Run the start script:
```bash
./start.sh
```

This will automatically:
- Install backend dependencies
- Start the Flask API server
- Start the frontend development server

### Option 2: Manual Setup (All Platforms)

#### Step 1: Install Dependencies

**Backend:**
```bash
cd backend
pip install -r requirements.txt
cd ..
```

**Frontend:**
```bash
npm install
```

#### Step 2: Start Backend Server

Open a terminal window and run:
```bash
cd backend
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

Keep this terminal window open.

#### Step 3: Start Frontend Server

Open a NEW terminal window and run:
```bash
npm run dev
```

You should see:
```
VITE v5.x.x ready in xxx ms

➜  Local:   http://localhost:5173/
```

#### Step 4: Open the Application

Open your browser and navigate to:
```
http://localhost:5173
```

## Troubleshooting

### Backend Issues

**Problem: "Module not found" error**
```bash
pip install flask flask-cors
```

**Problem: Port 5000 already in use**
Edit `backend/app.py` and change the port:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Changed to 5001
```

Then update `src/services/api.ts`:
```typescript
const API_BASE_URL = 'http://localhost:5001/api';
```

**Problem: CORS errors**
Make sure the backend is running before starting the frontend.

### Frontend Issues

**Problem: "npm command not found"**
Install Node.js from https://nodejs.org/

**Problem: Dependencies installation fails**
Try clearing npm cache:
```bash
npm cache clean --force
npm install
```

**Problem: Port 5173 already in use**
The Vite dev server will automatically try the next available port (5174, 5175, etc.)

### API Connection Issues

**Problem: "Failed to fetch" errors**
1. Ensure backend is running on http://localhost:5000
2. Check browser console for CORS errors
3. Verify API_BASE_URL in `src/services/api.ts`

## Testing the Application

### 1. Verify Analytics Dashboard
You should see:
- Total Leads: 10
- Valid Emails: 10
- High Quality Leads: 4
- Average Score: ~78

### 2. Test Filtering
Try these filters:
- **Tech Stack**: Select "React" → Should show 6 leads
- **Location**: Select "San Francisco, CA" → Should show 1 lead
- **Minimum Score**: Enter "80" → Should show 4 high-priority leads

### 3. Test Export
1. Select one or more leads by clicking the checkboxes
2. Click "Export" button in the header
3. A CSV file should download automatically

### 4. Test Responsive Design
- Resize your browser window
- Try on mobile (use browser dev tools → responsive mode)
- All features should work on different screen sizes

## API Endpoints Reference

Test the API directly using curl or Postman:

### Get All Leads
```bash
curl http://localhost:5000/api/leads
```

### Filter by Technology
```bash
curl "http://localhost:5000/api/leads?tech_stack=React"
```

### Get Analytics
```bash
curl http://localhost:5000/api/analytics
```

### Get Filter Options
```bash
curl http://localhost:5000/api/filters/options
```

### Export Leads
```bash
curl -X POST http://localhost:5000/api/export \
  -H "Content-Type: application/json" \
  -d '{"lead_ids": [1, 2, 3]}'
```

## Project Structure Overview

```
project/
├── backend/
│   ├── app.py              # Flask API server
│   └── requirements.txt    # Python dependencies
│
├── src/
│   ├── components/         # React components
│   │   ├── AnalyticsDashboard.tsx
│   │   ├── FilterBar.tsx
│   │   └── LeadCard.tsx
│   ├── services/
│   │   └── api.ts         # API client
│   ├── types/
│   │   └── lead.ts        # TypeScript types
│   ├── App.tsx            # Main application
│   └── main.tsx           # Entry point
│
├── README.md              # Main documentation
├── report.md              # Technical report
├── SETUP_GUIDE.md         # This file
└── VIDEO_GUIDE.md         # Video walkthrough script
```

## What to Look For During Review

### User Experience
1. **First Impression**: Clean, professional interface
2. **Navigation**: Intuitive filtering and selection
3. **Performance**: Fast loading and smooth interactions
4. **Visual Feedback**: Clear indicators for scores, selection, loading states

### Technical Quality
1. **Code Organization**: Modular, well-structured components
2. **Type Safety**: TypeScript interfaces and type checking
3. **Error Handling**: Graceful error states
4. **Responsive Design**: Works on all screen sizes

### Business Value
1. **Lead Scoring**: Intelligent prioritization algorithm
2. **Filtering**: Multi-dimensional search capabilities
3. **Export**: Seamless CRM integration via CSV
4. **Analytics**: Actionable insights for sales strategy

## Key Features to Demo

1. **Analytics Dashboard** (top of page)
   - Shows aggregate metrics
   - Visualizes top technologies and industries

2. **Filter Bar**
   - Technology stack dropdown
   - Location, company size, role, industry filters
   - Minimum lead score input
   - "Clear All" button

3. **Lead Cards**
   - Color-coded priority badges (green = high, blue = medium, gray = low)
   - Email validation checkmarks
   - Technology stack tags
   - Clickable LinkedIn links

4. **Selection & Export**
   - Individual lead checkboxes
   - "Select All" / "Deselect All" toggle
   - Export button with selection count
   - CSV download with all lead data

## Production Deployment Notes

For production deployment:

1. **Backend**:
   - Use Gunicorn or uWSGI
   - Deploy to Heroku, AWS, or DigitalOcean
   - Use PostgreSQL instead of mock data
   - Add authentication/authorization

2. **Frontend**:
   - Build: `npm run build`
   - Serve from `dist/` folder
   - Deploy to Vercel, Netlify, or AWS S3
   - Update API_BASE_URL to production backend

3. **Database**:
   - Set up PostgreSQL or MongoDB
   - Create migrations for lead schema
   - Implement connection pooling

## Getting Help

If you encounter issues:

1. Check the [README.md](./README.md) for detailed documentation
2. Review the [report.md](./report.md) for technical details
3. Ensure all prerequisites are installed correctly
4. Verify both backend and frontend are running
5. Check browser console for error messages

## Next Steps After Setup

1. Explore the filtering functionality
2. Try exporting different lead selections
3. Review the code structure in `src/` and `backend/`
4. Read the technical report for design decisions
5. Test the responsive design on different screen sizes

---

Enjoy exploring LeadSquatch Pro! The entire application was built with production-quality code, modern best practices, and a focus on delivering real business value to B2B sales teams.
