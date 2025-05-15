import React, { useState } from 'react';
import DataFetcher from './DataFetcher';
import CreateForm from './CreateForm';

function App() {
  const [selectedTable, setSelectedTable] = useState('');
  const [reload, setReload] = useState(false); // чтобы перезагрузить данные

  const tableOptions = [
    'clients',
    'drivers',
    'orders',
    'cars',
    'staff',
    'positions',
    'tech_inspection',
    'assignments',
    'orders_drivers'
  ];

  const handleReload = () => {
    setReload(prev => !prev); // сменим значение, чтобы обновить
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Выбор таблицы</h1>

      <select
        value={selectedTable}
        onChange={(e) => setSelectedTable(e.target.value)}
      >
        <option value="">-- Выберите таблицу --</option>
        {tableOptions.map((table) => (
          <option key={table} value={table}>
            {table}
          </option>
        ))}
      </select>

      {selectedTable && (
        <>
          <DataFetcher table={selectedTable} reload={reload} />
          <CreateForm table={selectedTable} onSuccess={handleReload} />
        </>
      )}
    </div>
  );
}

export default App;
