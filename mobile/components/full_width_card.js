
import React from 'react';
import {Dimensions} from 'react-native';
import {Card} from "@rneui/base";

function FullWidthCard({
    gap = {horizontal: 0},
    borderRadius = {topLeft: 0, topRight: 0},
    children,
}){
    return (
        <Card
            // containerStyle={{
            //     width: Dimensions.get('window').width - gap.horizontal,
            //     borderTopLeftRadius: borderRadius.topLeft,
            //     borderTopRightRadius: borderRadius.topRight,
            //     children,
            // }}
        >
            {children}
        </Card>
    );
};

export default FullWidthCard;