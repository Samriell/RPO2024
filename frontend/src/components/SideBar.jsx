import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Nav, Button } from 'react-bootstrap';
import { faBars, faGlobe } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import '.././App.css';

const SideBar = props => {
    const [expanded, setExpanded] = useState(false);

    const toggleSidebar = () => {
        setExpanded(!expanded);
    };

    return (
        <>
            <Button className="sidebar-toggle" onClick={toggleSidebar}>
                <FontAwesomeIcon icon={faBars} />
            </Button>
            <Nav className={`my-sidebar ${expanded ? 'expanded' : 'collapsed'}`}>
                <Nav.Item>
                    <Nav.Link as={Link} to="/countries">
                        <FontAwesomeIcon icon={faGlobe} />{' '}Страны
                    </Nav.Link>
                </Nav.Item>
            </Nav>
        </>
    );
}

export default SideBar;
