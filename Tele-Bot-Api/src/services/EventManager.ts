import EventEmitter from 'node:events';

class EventManager extends EventEmitter {
  constructor() {
    super();
  }
}

export const eventManager = new EventManager();
