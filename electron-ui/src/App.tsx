import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from "@/components/ui/label"
import { Card, CardAction, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "./components/ui/card"
import { useNavigate } from 'react-router-dom'
import { useUser } from '@/context/user-context'

function Authenticate() {
  const navigate = useNavigate()
  const { setUserId } = useUser()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)

    if (username === 'debug_user') {
      try {
        const res = await fetch('/api/db-api/create-debug-user')
        if (!res.ok) {
          setError('Failed to create debug user.')
          return
        }
        const data = await res.json()
        setUserId(data.id)
        navigate('/home')
      } catch {
        setError('Could not reach the server.')
      }
      return
    }

    setError('Invalid credentials.')
  }

  return (
    <main className="flex min-h-svh w-full items-center justify-center px-4 py-8">
      <Card className="login-card-enter w-full max-w-md shadow-lg">
        <CardHeader>
          <CardTitle>Login to your account</CardTitle>
          <CardDescription>
            Enter your credentials to login
          </CardDescription>
          <CardAction>
            <Button variant="link">Sign Up</Button>
          </CardAction>
        </CardHeader>
        <CardContent>
          <form id="login-form" onSubmit={handleSubmit}>
            <div className="flex flex-col gap-6">
              <div className="grid gap-2">
                <Label htmlFor="username">Username</Label>
                <Input
                  id="username"
                  type="text"
                  placeholder="username"
                  value={username}
                  onChange={e => setUsername(e.target.value)}
                  required
                />
              </div>
              <div className="grid gap-2">
                <div className="flex items-center">
                  <Label htmlFor="password">Password</Label>
                  <a href="#" className="ml-auto inline-block text-sm underline-offset-4 hover:underline">
                    Forgot your password?
                  </a>
                </div>
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  required
                />
              </div>
              {error && <p className="text-sm text-destructive">{error}</p>}
            </div>
          </form>
        </CardContent>
        <CardFooter>
          <Button type="submit" form="login-form" className="w-full">
            Login
          </Button>
        </CardFooter>
      </Card>
    </main>
  )
}

export default Authenticate
