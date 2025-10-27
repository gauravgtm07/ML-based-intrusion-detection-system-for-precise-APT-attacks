import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://wqraewjvojhyeqemiavm.supabase.co'
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndxcmFld2p2b2poeWVxZW1pYXZtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE1NTE2NzgsImV4cCI6MjA3NzEyNzY3OH0.1048LVo53YAaDXrgKax6VRxWgbIOVr43q73SoIFOM6A'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
