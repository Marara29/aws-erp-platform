import { useEffect, useState } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'
const MODULES = ['employees', 'inventory', 'orders', 'reports']

export default function App() {
  const [activeModule, setActiveModule] = useState('employees')
  const [payload, setPayload] = useState(null)
  const [loading, setLoading] = useState(false)

  const [orderForm, setOrderForm] = useState({
    order_number: '',
    customer_name: '',
    total_amount: '',
    status: 'PENDING'
  })

  const fetchModule = async () => {
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/${activeModule}`)
      const json = await res.json()
      setPayload(json)
    } catch {
      setPayload({ error: 'Unable to reach backend API. Start FastAPI at :8000.' })
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchModule()
  }, [activeModule])

  const createOrder = async (e) => {
    e.preventDefault()

    const res = await fetch(`${API_BASE}/orders`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        order_number: orderForm.order_number,
        customer_name: orderForm.customer_name,
        total_amount: Number(orderForm.total_amount),
        status: orderForm.status
      })
    })

    const json = await res.json()
    alert(json.message)

    setOrderForm({
      order_number: '',
      customer_name: '',
      total_amount: '',
      status: 'PENDING'
    })

    setActiveModule('orders')
    fetchModule()
  }

  return (
    <div className="container">
      <header>
        <h1>My AWS ERP Test </h1>
        <p>React + FastAPI + PostgreSQL (practice stack for AWS).</p>
      </header>

      <nav>
        {MODULES.map((module) => (
          <button
            key={module}
            className={module === activeModule ? 'active' : ''}
            onClick={() => setActiveModule(module)}
          >
            {module}
          </button>
        ))}
      </nav>

      <section>
        {activeModule === 'orders' && (
          <form onSubmit={createOrder} className="order-form">
            <h2>Create Customer Order</h2>

            <input
              placeholder="Order Number"
              value={orderForm.order_number}
              onChange={(e) =>
                setOrderForm({ ...orderForm, order_number: e.target.value })
              }
            />

            <input
              placeholder="Customer Name"
              value={orderForm.customer_name}
              onChange={(e) =>
                setOrderForm({ ...orderForm, customer_name: e.target.value })
              }
            />

            <input
              type="number"
              placeholder="Total Amount"
              value={orderForm.total_amount}
              onChange={(e) =>
                setOrderForm({ ...orderForm, total_amount: e.target.value })
              }
            />

            <select
              value={orderForm.status}
              onChange={(e) =>
                setOrderForm({ ...orderForm, status: e.target.value })
              }
            >
              <option value="PENDING">PENDING</option>
              <option value="SHIPPED">SHIPPED</option>
              <option value="DELIVERED">DELIVERED</option>
              <option value="CANCELLED">CANCELLED</option>
            </select>

            <button type="submit">Create Order</button>
          </form>
        )}

        {loading && <p>Loading {activeModule}…</p>}
        {!loading && <pre>{JSON.stringify(payload, null, 2)}</pre>}
      </section>
    </div>
  )
}
