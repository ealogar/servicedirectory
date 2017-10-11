db.apis.update(
{"_id": "sms"},
{
  $set : {
  "rules":
      [
        {    
            "client_name": "tume",
            "binding_rules":[
                 {
                 "group_rules": [{"operation":"range", "input_context_param":"uuid", "value":[100, 500]},
                           {"operation":"eq", "input_context_param":"ob", "value":["es"]}],
                 "bindings": ["51c577679078b9023b3a2c4b"] 
                 },
                 {
                 "group_rules": [{"operation":"eq", "input_context_param":"ob", "value":["es"]},
                           {"operation":"eq", "input_context_param":"premium", "value":[true]}],
                 "bindings": ["51c576c09078b9023b3a2c4a"] 
                 },
                 {
                 "group_rules": [{"operation":"eq", "input_context_param":"ob", "value":["es"]},
                           {"operation":"eq", "input_context_param":"premium", "value":[false]}],
                 "bindings": ["51cab6419078b918f6504344"] 
                 },                 
                 {
                 "group_rules": [],
                 "bindings": ["51c18932469904195c0ba355"] 
                 }
            ]
        },
        {
            "client_name": "default",
            "binding_rules":[
                 {
                 "group_rules": [{"operation":"in", "input_context_param":"ob", "value":["es", "de", "uk"]},
                           {"operation":"eq", "input_context_param":"premium", "value":[true]}],
                 "bindings": ["51c576c09078b9023b3a2c4a"] 
                 },
                 {
                 "group_rules": [{"operation":"regex", "input_context_param":"ob", "value":["[a-zA-Z]{2}"]},
                           {"operation":"eq", "input_context_param":"premium", "value":[false]}],
                 "bindings": ["51c5766c9078b9023b3a2c49", "51e5aef0f26ba33234fd8e52"] 
                 }
            ]
        }
      ]
  }
  
}
)

