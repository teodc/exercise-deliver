const CreateDelivery = (props) => {
    const submit = async (e) => {
        e.preventDefault();
        const form = new FormData(e.target);
        const data = Object.fromEntries(form.entries());
        const response = await fetch(process.env.REACT_APP_BACKEND_URL + "/create-delivery", {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const { detail } = await response.json();
            alert(detail);
            return;
        }

        const { delivery_id } = await response.json();
        props.setDeliveryId(delivery_id);
    }

    return (
        <div className="columns is-mobile">
            <div className="column is-half is-offset-one-quarter">
                <h2 className="title is-2">Welcome!</h2>
                <form className="card" onSubmit={submit}>
                    <header className="card-header">
                        <p className="card-header-title">Create Delivery</p>
                    </header>
                    <div className="card-content">
                        <div className="field">
                            <div className="control">
                                <input className="input" type="number" name="budget" placeholder="Budget" />
                            </div>
                        </div>
                        <div className="field">
                            <div className="control">
                                <input className="input" type="text" name="notes" placeholder="Notes" />
                            </div>
                        </div>
                        <button className="button is-primary">Submit</button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default CreateDelivery;
