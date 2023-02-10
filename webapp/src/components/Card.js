function Card(props) {
  return (
          <>
            <div className="col-md-4">
              <img src={props.item.imgAddr} width="80%" alt=""/>
              <h4>{props.item.title}</h4>
              <p>{props.item.price}</p>
            </div>
          </>
  )
}

export default Card;