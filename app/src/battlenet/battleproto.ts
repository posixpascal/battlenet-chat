import * as protobuf from 'protobufjs';

// TODO: this is rather ugly, not sure why I do this... :<
export interface BattleProto extends Object {
  account? : {
    AccountCredential? :  protobuf.ReflectionObject
  };
}
