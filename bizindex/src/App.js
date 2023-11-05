import './App.css';
import { Route, Routes} from "react-router-dom";
import Navbar from "./components/navbar";
import Footer from "./components/footer";
import Info from "./components/info";
import BusinessIndex from "./components/businessIndex";

function App() {
    return (
        <div className='App'>
            <Navbar/>
            <Routes>
                <Route path="/" element={<BusinessIndex/>}/>
                <Route path="/about" element={<Info/>}/>
            </Routes>
            <Footer/>
        </div>
    );
}

export default App;
