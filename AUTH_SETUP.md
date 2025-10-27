# 🔐 Authentication Setup Guide

## Overview

This project now includes a complete authentication system powered by **Supabase**. Users must sign up and log in before accessing the IDS Dashboard.

## Features

✅ **User Registration** - Create new accounts with email and password  
✅ **User Login** - Secure authentication with Supabase  
✅ **Session Management** - Automatic session handling and persistence  
✅ **Logout** - Sign out functionality with one click  
✅ **Protected Routes** - Dashboard is only accessible to authenticated users  
✅ **Beautiful UI** - Modern, gradient-based login/signup pages  

## Configuration

### Supabase Credentials

The following Supabase credentials are already configured in the project:

- **Supabase URL**: `https://wqraewjvojhyeqemiavm.supabase.co`
- **Anon Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndxcmFld2p2b2poeWVxZW1pYXZtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE1NTE2NzgsImV4cCI6MjA3NzEyNzY3OH0.1048LVo53YAaDXrgKax6VRxWgbIOVr43q73SoIFOM6A`

These are configured in: `frontend/src/lib/supabase.ts`

## How It Works

### 1. Authentication Flow

```
User visits app → Login/Signup page → Enter credentials → 
Supabase validates → Session created → Access granted to Dashboard
```

### 2. Components Structure

```
frontend/src/
├── lib/
│   └── supabase.ts              # Supabase client configuration
├── contexts/
│   └── AuthContext.tsx          # Authentication context provider
├── components/
│   └── Auth/
│       ├── Login.tsx            # Login page component
│       ├── Signup.tsx           # Signup page component
│       └── AuthWrapper.tsx      # Authentication guard component
```

### 3. Key Files Modified

- **`main.tsx`** - Wrapped with `AuthProvider`
- **`App.tsx`** - Wrapped with `AuthWrapper` to protect routes
- **`Header.tsx`** - Added user email display and logout button

## Usage

### For Users

1. **First Time Users**:
   - Click "Sign up" on the login page
   - Enter your email and password (min 6 characters)
   - Confirm your password
   - Click "Sign Up"
   - You'll be redirected to login

2. **Returning Users**:
   - Enter your email and password
   - Click "Sign In"
   - Access the dashboard

3. **Logging Out**:
   - Click the "Logout" button in the top-right corner of the dashboard

### For Developers

#### Using the Auth Context

```tsx
import { useAuth } from './contexts/AuthContext'

function MyComponent() {
  const { user, signIn, signUp, signOut } = useAuth()
  
  // user contains the current authenticated user
  // or null if not authenticated
}
```

#### Protecting Routes

Routes are automatically protected by the `AuthWrapper` component. Any component wrapped in `AuthWrapper` requires authentication.

## Security Notes

🔒 **Password Requirements**: Minimum 6 characters  
🔒 **Session Storage**: Sessions are stored securely by Supabase  
🔒 **Automatic Logout**: Sessions expire based on Supabase configuration  
🔒 **API Keys**: The anon key is safe to expose in frontend code  

## Troubleshooting

### Issue: "Invalid login credentials"
- **Solution**: Double-check your email and password
- Make sure you've created an account first

### Issue: Can't sign up
- **Solution**: Check if the email is already registered
- Ensure password is at least 6 characters

### Issue: Session not persisting
- **Solution**: Check browser cookies are enabled
- Clear browser cache and try again

## Testing

To test the authentication:

1. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

2. Visit `http://localhost:5173`
3. You should see the login page
4. Create a new account or login with existing credentials

## Supabase Dashboard

To manage users and authentication settings, visit your Supabase dashboard:
- URL: https://app.supabase.com/project/wqraewjvojhyeqemiavm

From there you can:
- View registered users
- Configure email templates
- Set up email verification
- Manage authentication providers
- Configure session settings

## Next Steps

Potential enhancements:
- ✨ Email verification
- ✨ Password reset functionality
- ✨ Social login (Google, GitHub, etc.)
- ✨ Two-factor authentication
- ✨ User profile management
- ✨ Role-based access control

---

**Note**: The authentication system is fully integrated and does not affect any existing functionality of the IDS system. All monitoring, alerts, and dashboard features work exactly as before, but now require authentication.
