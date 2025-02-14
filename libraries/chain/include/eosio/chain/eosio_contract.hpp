#pragma once

#include <eosio/chain/types.hpp>
#include <eosio/chain/contract_types.hpp>

namespace eosio { namespace chain {

   class apply_context;

   /**
    * @defgroup native_action_handlers Native Action Handlers
    */
   ///@{
   void apply_gax_newaccount(apply_context&);
   void apply_gax_updateauth(apply_context&);
   void apply_gax_deleteauth(apply_context&);
   void apply_gax_linkauth(apply_context&);
   void apply_gax_unlinkauth(apply_context&);

   /*
   void apply_eosio_postrecovery(apply_context&);
   void apply_eosio_passrecovery(apply_context&);
   void apply_eosio_vetorecovery(apply_context&);
   */

   void apply_gax_setcode(apply_context&);
   void apply_gax_setabi(apply_context&);

   void apply_gax_canceldelay(apply_context&);

   void apply_gax_xshout(apply_context&);
   void apply_gax_xshin(apply_context&);
   ///@}  end action handlers

} } /// namespace eosio::chain
