import { useEffect, useState } from 'react';

const ManageDelivery = (props) => {
    const [state, setState] = useState({});
    const [refresh, setRefresh] = useState(false);

    useEffect(() => {
        (async () => {
            const response = await fetch(process.env.REACT_APP_BACKEND_URL + "/get-status/" + props.deliveryId);

            if (!response.ok) {
                const { detail } = await response.json();
                alert(detail);
                return;
            }

            const data = await response.json();
            setState(data);
        })()
    }, [refresh]);

    const submit = async (e, endpoint) => {
        e.preventDefault();
        const form = new FormData(e.target);
        const data = Object.fromEntries(form.entries());
        const response = await fetch(process.env.REACT_APP_BACKEND_URL + endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ delivery_id: props.deliveryId, ...data })
        });

        if (!response.ok) {
            const { detail } = await response.json();
            alert(detail);
            return;
        }

        setRefresh(!refresh);
    }

    function Progress(props) {
        switch (props.status) {
            case 'ready':
                return <progress className="progress my-5 is-large is-primary" value="0" max="100"></progress>
            case 'in_progress':
                return <progress className="progress my-5 is-large is-primary" value="33" max="100"></progress>
            case 'collected':
                return <progress className="progress my-5 is-large is-primary" value="66" max="100"></progress>
            case 'completed':
                return <progress className="progress my-5 is-large is-primary" value="100" max="100"></progress>
            default:
                return <progress className="progress my-5 is-large is-warning" max="100"></progress>
        }
    }

    return (
        <div>
            <h2 className="title is-2">Delivery Status</h2>
            <h4 className="subtitle is-5">
                ID: {state.delivery_id}
                <br />
                Status: {state.status}
            </h4>

            <Progress status={state.status} />

            <div className="columns my-5">
                <div className="column">
                    <form className="card" onSubmit={e => submit(e, "/start-delivery")}>
                        <header className="card-header">
                            <p className="card-header-title">Start Delivery</p>
                        </header>
                        <div className="card-content">
                            <button className="button is-primary">Submit</button>
                        </div>
                    </form>
                </div>
                <div className="column">
                    <form className="card" onSubmit={e => submit(e, "/increase-budget")}>
                        <header className="card-header">
                            <p className="card-header-title">Increase Budget</p>
                        </header>
                        <div className="card-content">
                            <div className="field">
                                <div className="control">
                                    <input className="input" type="number" name="amount" placeholder='Amount' />
                                </div>
                            </div>
                            <button className="button is-primary">Submit</button>
                        </div>
                    </form>
                </div>
                <div className="column">
                    <form className="card" onSubmit={e => submit(e, "/pickup-products")}>
                        <header className="card-header">
                            <p className="card-header-title">Pickup Products</p>
                        </header>
                        <div className="card-content">
                            <div className="field">
                                <div className="control">
                                    <input className="input" type="number" name="purchase_price" placeholder="Purchase Price" />
                                </div>
                            </div>
                            <div className="field">
                                <div className="control">
                                    <input className="input" type="number" name="quantity" placeholder="Quantity" />
                                </div>
                            </div>
                            <button className="button is-primary">Submit</button>
                        </div>
                    </form>
                </div>
                <div className="column">
                    <form className="card" onSubmit={e => submit(e, "/deliver-products")}>
                        <header className="card-header">
                            <p className="card-header-title">Deliver Products</p>
                        </header>
                        <div className="card-content">
                            <div className="field">
                                <div className="control">
                                    <input className="input" type="number" name="sell_price" placeholder="Sell Price" />
                                </div>
                            </div>
                            <div className="field">
                                <div className="control">
                                    <input className="input" type="number" name="quantity" placeholder="Quantity" />
                                </div>
                            </div>
                            <button className="button is-primary">Submit</button>
                        </div>
                    </form>
                </div>
            </div>

            <code>
                {JSON.stringify(state)}
            </code>

        </div>
    );
};

export default ManageDelivery;
