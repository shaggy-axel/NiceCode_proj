function dragStart(ev) {
    // dragstart
    // Срабатывает когда элeмент начал перемещаться.
    // В момент срабатывания события dragstart пользователь начинает перетаскивание элемента.
    // Обработчик данного события может быть использован для сохранения информации о перемещаемом объекте,
    // а также для изменения изображения,
    // которое будет ассоциировано с перемещением.
    // Дaнное событие не срабатывает,
    // когда некоторый файл будет переноситься из операционной системы в браузер.
    // Для детальной информации Starting a Drag Operation.
    // https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API/Drag_operations#dragstart
    ev.dataTransfer.effectAllowed = 'move';
    ev.dataTransfer.setData("Text", ev.target.getAttribute('id'));
    ev.dataTransfer.setDragImage(ev.target, 100, 100);
    return true;
}

function dragEnter(ev) {
    //dragenter
    // Срабатывает, когда перемещаемый элемент попадает на элемент-назначение.
    // Обработчик этого события показывает,
    // что элемент находится над объектом на который он может быть перенесен.
    // Если же обработчика нет,
    // либо он не совершает никаких действий перемещение по умолчанию запрещено.
    // Это событие также используется для того,
    // чтобы подсветить либо промаркировать объект над которым происходит перемещения в случае,
    // если перемещение на данный элемент разрешено.
    // Для детальной информации смотрите Specifying Drop Targets.
    // https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API/Drag_operations#droptargets
    ev.preventDefault();
    return true;
}

function dragOver(ev) {
    //  dragover
    //Данное событие срабатывает каждые несколько сотен милисекунд,
    // когда перемещаемый элемент оказывается над зоной, принимающей перетаскиваемые элементы.
    // Для детальной информации смотрите Specifying Drop Targets.
    // https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API/Drag_operations#droptargets
    event.preventDefault();
}

function dragDrop(ev) {
    //drop
    // Событие drop вызывается для элемента, над которым произошло "сбрасывание" перемещаемого элемента.
    // Событие отвечает за извлечение "сброшенных" данных и их вставку.
    // Событие будет срабатывать только при завершении операции перетаскивания, например, событие не сработает,
    // если пользователь отменит перетаскивание нажатием Esc, или не донесет элемент, до цели.
    // Для детальной информации смотрите Performing a Drop.
    // https://developer.mozilla.org/en-US/docs/DragDrop/Drag_Operations#drop
    const data = ev.dataTransfer.getData("Text");
    ev.target.appendChild(document.getElementById(data));
    ev.stopPropagation();
    return false;
}
