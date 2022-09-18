import { useState } from 'react';
import CreateDelivery from './CreateDelivery';
import ManageDelivery from './ManageDelivery';

function App() {
  const [deliveryId, setDeliveryId] = useState('');

  return (
    <div className="App py-5">
      <div className="container">
        {
          deliveryId === ''
            ? <CreateDelivery setDeliveryId={setDeliveryId} />
            : <ManageDelivery deliveryId={deliveryId} />
        }
      </div>
    </div>
  );
}

export default App;
