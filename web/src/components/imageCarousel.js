import {Image, Segment} from "semantic-ui-react";
import Carousel from "semantic-ui-carousel-react";

export default function ImageCarousel(image_urls){
    let elements = [];
    image_urls.forEach((image_url) => {
        elements.push(
            {render: () => {return <Image centered src={image_url} />}}
        )
    });

    return (
        <Segment>
            <Carousel
                elements={elements}
                animation="fade"
                showNextPrev={false}
                showIndicators={true}
            />
        </Segment>
    );
}