import React, { useRef } from "react";
import { Link } from "react-router-dom";
import "./Feed.css";
import { BACKEND_URL } from "./vars";
import store from "./store";
import { useEffect } from "react";

function Feed({ translations }) {
	const [headers, setHeaders] = React.useState([]);
	const stillOnPage = useRef(true)

	useEffect(() => {
		const fetchHeaders = async () => {
			try {
				const response = await fetch(`${BACKEND_URL}/get-headers/${store.getState().user.token}`, {
					method: "GET",
					headers: {
						"Content-Type": "application/json",
					},
				});
				const data = await response.json();
				const newHeaders = data.headlines
				setHeaders(newHeaders);
			} catch (error) {
				console.error("Error fetching headers:", error);
			}
		};

		fetchHeaders();
	}, []);

	useEffect(() => {
		console.log("Starting audio...");

		stillOnPage.current = true;
		const audioUrl = `${BACKEND_URL}/get-audio/${store.getState().user.token}`
		let audio = null;
		let audioPromise = null;

		audio = new Audio(audioUrl);
		if (stillOnPage.current) {
			audioPromise = audio.play();
		}

		return () => {
			stillOnPage.current = false; // prevent audio playing in background

			if (audioPromise) {
				audioPromise.then(() => {
					console.log('stopping background audio...')
					audio.pause();
				});
			}
		}
	}, [])

	return (
		<div className="feed-container">
			{/* Home button at the top center */}
			<div className="home-button-container">
				<Link to="/">
					<button className="home-button">{translations ? translations.homeTitle : "Home"}</button>
				</Link>
			</div>

			{/* Feed page content */}
			<h1 className="feed-title">{translations ? translations.feedButton : "Feed Page"}</h1>

			{/* Use the translations prop for the paragraph content */}
			<div className="feed-subtitle-container">
				<p className="feed-subtitle">
					{translations ? translations.feedContent : "Here is what is happening today:"}
				</p>
			</div>
			<div>
				<ul>
					{headers.map((headline, index) => (
						<li key={index}>
							<h3>{headline}</h3>
						</li>
					))}
				</ul>
			</div>
		</div>
	);
}

export default Feed;
