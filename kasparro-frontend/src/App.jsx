import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { RefreshCw, Database, TrendingUp, Search } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await axios.get('https://kasparro-backend-subhali-ar-otti.onrender.com/data');
      setData(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchData();
  }, []);

  // P1.2 Logic: Filter data based on search term (Source or Asset)
  const filteredData = data.filter(item => 
    item.source.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.asset.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div style={{ padding: '0', backgroundColor: '#f3f4f6', minHeight: '100vh', width: '100vw', fontFamily: 'sans-serif', overflowX: 'hidden' }}>
      
      {/* Header - Full Width */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', backgroundColor: 'white', padding: '20px 40px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)', marginBottom: '20px' }}>
        <h1 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '10px', fontSize: '24px', color: '#1f2937' }}>
          <Database color="#4f46e5" size={28} /> Kasparro ETL Dashboard
        </h1>
        
        <div style={{ display: 'flex', gap: '15px' }}>
          {/* Search Input (Requirement P1.2) */}
          <div style={{ position: 'relative' }}>
            <Search style={{ position: 'absolute', left: '12px', top: '10px', color: '#9ca3af' }} size={20} />
            <input 
              type="text" 
              placeholder="Search source or asset..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{ padding: '10px 15px 10px 40px', borderRadius: '8px', border: '1px solid #e5e7eb', width: '250px', outline: 'none' }}
            />
          </div>

          <button onClick={fetchData} style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '12px 24px', backgroundColor: '#4f46e5', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>
            <RefreshCw size={18} className={loading ? 'animate-spin' : ''} /> Refresh Data
          </button>
        </div>
      </div>

      {/* Main Content Layout */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '30px', padding: '0 30px' }}>
        
        {/* Left Side: Table (Matches data from image_ad7581.png) */}
        <div style={{ backgroundColor: 'white', padding: '25px', borderRadius: '16px', boxShadow: '0 4px 6px rgba(0,0,0,0.05)' }}>
          <h3 style={{ marginTop: 0, color: '#374151', marginBottom: '20px' }}>Stored Price Data</h3>
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ textAlign: 'left', borderBottom: '2px solid #f3f4f6', color: '#6b7280', fontSize: '13px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  <th style={{ padding: '15px' }}>Source</th>
                  <th style={{ padding: '15px' }}>Asset</th>
                  <th style={{ padding: '15px' }}>Price (USD)</th>
                </tr>
              </thead>
              <tbody>
                {filteredData.length > 0 ? (
                  filteredData.map(item => (
                    <tr key={item.id} style={{ borderBottom: '1px solid #f9fafb' }}>
                      <td style={{ padding: '15px', fontWeight: 'bold', color: '#111827' }}>{item.source.toUpperCase()}</td>
                      <td style={{ padding: '15px', color: '#4b5563' }}>{item.asset}</td>
                      <td style={{ padding: '15px', fontWeight: '600', color: '#059669' }}>
                        ${item.price_usd.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="3" style={{ padding: '30px', textAlign: 'center', color: '#9ca3af' }}>No matching records found</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Right Side: Visualization (Matches chart from image_ad8809.png) */}
        <div style={{ backgroundColor: 'white', padding: '25px', borderRadius: '16px', boxShadow: '0 4px 6px rgba(0,0,0,0.05)' }}>
          <h3 style={{ marginTop: 0, display: 'flex', alignItems: 'center', gap: '8px', color: '#374151', marginBottom: '20px' }}>
            <TrendingUp color="#10b981" /> Market Comparison
          </h3>
          <div style={{ height: '400px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={filteredData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
                <XAxis dataKey="source" tick={{fill: '#6b7280', fontSize: 12}} axisLine={false} tickLine={false} />
                <YAxis tick={{fill: '#6b7280', fontSize: 12}} axisLine={false} tickLine={false} />
                <Tooltip 
                  cursor={{fill: '#f9fafb'}} 
                  contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px rgba(0,0,0,0.1)'}} 
                />
                <Bar dataKey="price_usd" fill="#4f46e5" radius={[6, 6, 0, 0]} barSize={50} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </div>
  );
}

export default App;